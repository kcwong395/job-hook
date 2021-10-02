import logging
from typing import List, Optional

from src.scraper.scraper import Scraper
from src.model.job import Job


class ScraperSG(Scraper):

    url = "https://careers.societegenerale.com/en/search?refinementList%5BjobLocation%5D%5B0%5D=Hong%20Kong"

    def __init__(self, target: str, url: str = url):
        super().__init__(target, url)

    """
        This func aims at closing the cookie page by clicking the agree button
        id -> The id of the agree button element
        delay -> A delay value for waiting elements to be loaded
    """
    def bypass_cookie(self, button_id: str, delay: int = None) -> None:
        delay = delay or self.delay
        agree_btn = self._driver.find_element_by_id(button_id)
        if not agree_btn:
            # this happens if id is not provided and agree button is not found
            raise Exception('Agree Cookie Button not found')
        agree_btn.click()
        self._driver.implicitly_wait(delay)
        logging.info('scraper bypassed cookie')

    """
        This func aims to find out how many jobs to scrap at the root page, as sometimes there might be multiple pages
        Knowing the total number of jobs can let the scraper know when to stop
    """
    def get_total_jobs(self) -> int:
        job_stat = self._driver.find_element_by_id("standalone-stats")
        job_stat_args = job_stat.text.split()
        if len(job_stat_args) > 0:
            job_num = job_stat_args[0].strip()
            if job_num.isnumeric():
                logging.info(job_num + " jobs are found")
                return int(job_num)
        raise Exception('Failed to retrieve total number of jobs')

    """
        This func finds out links for all the job details
    """
    def get_all_jobs_pages(self, trial: int = 15, total_job_num: int = 0) -> List[str]:
        job_links = []
        while trial > 0 and len(job_links) < total_job_num:
            job_links = self._driver.find_elements_by_class_name('viewjob')
            self.scroll()
            trial -= 1
            logging.info("Trial " + str(trial) + ": Current Jobs retrieved: " + str(len(job_links)))
        if len(job_links) <= 0:
            raise Exception('No job retrieved')
        if len(job_links) < total_job_num:
            logging.warning("Job retrieved less than expected, consider to input a higher value for trial")
        return [link.get_attribute('href') for link in job_links]

    def get_job_details_from_page(self, job_link: str) -> Optional[Job]:
        try:
            self.redirect(url=job_link)
            content = self.get_content()
            spans = content.find(class_="job-infos").find_all("span")

            # obtains all fields of the job details
            job = Job()
            job.ref = content.find(id="jobID").strong.text
            job.title = content.find(class_="page-title-medium").h1.text
            job.location = spans[0].text.replace("\n", "")
            job.job_type = spans[1].text.replace("\n", "")
            job.department = spans[2].text.replace("\n", "")
            job.start_date = content.find("span", text="Starting date:").find_next_sibling("span").strong.text
            job.publish_date = content.find("span", text="Publication date:").find_next_sibling("span").strong.text
            # job.qualification = content.find("div", class_="joboffer-qualification").text.replace("\n", "")

            logging.info(job.__dict__)
            return job
        except Exception as e:
            logging.error("Error Occur when scraping: " + job_link + ", ", e)
            return None

    # find all positions offered by SG-HK
    def start(self):
        logging.info(self.target + " scraper started")
        try:
            self.redirect(self.url)

            # bypass the cookie agreement page
            self.bypass_cookie("didomi-notice-agree-button")

            total_job_num = self.get_total_jobs()
            job_links = self.get_all_jobs_pages(total_job_num=total_job_num)

            job_list = [self.get_job_details_from_page(link) for link in job_links[:]]
            filter(lambda job: job is not None, job_list)
        except Exception as e:
            logging.error(e)
        logging.info(self.target + " scraper completed")
        self.shutdown()

