class Job:
    def __init__(self, _id: str, ref: str, job_type: str, title: str, department: str, location: str, start_date: str,
                 publish_date: str, link: str):
        self._id = _id
        self.ref = ref
        self.job_type = job_type
        self.title = title
        self.department = department
        self.location = location
        self.start_date = start_date
        self.publish_date = publish_date
        self.link = link


