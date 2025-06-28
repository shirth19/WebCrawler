from multiprocessing import Process
import sys
import util

class JobPosting(object):
    '''
    Holds basic information for each job posting
    '''
    def __init__(self, post, base_url):
        self.ID = post['id']
        
        #we can extract generally useful information from 'text' keys
        labels = list(util.extract_all_keys(post, 'text'))
        self.info = {'labels': labels}

        self.url = base_url + post['title']['commandLink']

def get_job_postings(main_link, dest_dir, thread_count, verbose):

    postings_page_dic = util.get_request_to_dic(main_link, verbose)

    #find the pagination end point
    end_points = util.extract_key(postings_page_dic, 'endPoints')
    base_url = main_link.split('.com')[0] + '.com'
    pagination_end_point = base_url
    pagination_key = "Pagination"

    if not end_points:
        if verbose:
            print("Unable to locate pagination endpoint; check the URL or site structure")
        return

    for end_point in end_points:
        if end_point['type'] == pagination_key:
            pagination_end_point += end_point['uri'] + '/'
            break


    #paginate until we have all the postings
    if verbose:
        print("Scraping list of all job postings..\n")
    job_postings = []
    while True:

        #attempt to retrieve list of job postings from json response
        postings_list = util.extract_key(postings_page_dic, 'listItems')
        if postings_list is None:
            break
        
        paginated_urls = [JobPosting(post, base_url) for post in postings_list]

        job_postings += paginated_urls

        postings_page_dic = util.get_request_to_dic(pagination_end_point + str(len(job_postings)), verbose)

    if verbose:
        print("\nThere are", len(job_postings), "job postings.\n")
        print("Scraping full descriptions of each job posting..\n")
    threads = []
    for i in range(thread_count):
        start = int(i * len(job_postings) / thread_count)
        end = int((i+1) * len(job_postings) / thread_count)
        thread = Process(target=get_job_description, args=(job_postings, start, end, dest_dir, verbose))
        threads.append(thread)
        thread.start()

    for i in range(thread_count):
        threads[i].join()

    if verbose:
        print("\nDone. All files stored under", dest_dir)

def get_job_description(job_postings, start, end, dest_dir, verbose=False):
    '''
    Iterates through [start, end) portion of the job postings, retrieves their full description, and writes to file

    Input:
        job_postings: list of JobPosting
        start: start index
        end: end index
        dest_dir: write path for file storage
    Returns:
        No return, writes to file
    '''
    for i in range(start, end):
        job_posting = job_postings[i]
        job_page_dic = util.get_request_to_dic(job_posting.url, verbose)
        description = util.extract_key(job_page_dic, 'description')
        job_info = job_posting.info
        job_info['description'] = description
        util.write_to_file(job_posting.ID, job_info, dest_dir)





def read_command(argv):
    """Parse command-line options using argparse."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Scrape job postings from a Workday job board.'
    )
    parser.add_argument(
        '-u', '--url', dest='main_link',
        default='https://mastercard.wd1.myworkdayjobs.com/CorporateCareers',
        help='Job Posting URL'
    )
    parser.add_argument(
        '-d', '--dest', dest='dest_dir',
        default='./test',
        help='Destination Directory'
    )
    parser.add_argument(
        '-t', '--threads', dest='thread_count', type=int,
        default=4,
        help='Number of parallel threads'
    )
    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true',
        default=False,
        help='Verbose output to sdout'
    )

    args = parser.parse_args(argv)
    return vars(args)

if __name__ == '__main__':
    options = read_command(sys.argv[1:])
    get_job_postings(**options)
