import numpy as np
import datetime as dt
import json
import pprint as pp


class Job:
    PU_TW_LENGTH = 15  # minutes
    DO_TW_LENGTH = 30  # minutes

    def __init__(self, job):
        for key in job:
            setattr(self, key, job[key])

        self.pu_tw = {'start': -1, 'end': -1}
        self.do_tw = {'start': -1, 'end': -1}
        self.pu_tw['start'] = self.do_tw['start'] = self._get_pickup_at(job['pickup_at'])
        self._set_pu_tw_end()
        self._set_do_tw_end()

    def _get_pickup_at(self, pickup_at):
        """
        Get the pickup_at whether the job is instant or scheduled

        :return: pickup_at datetime
        """
        if not pickup_at:
            return dt.datetime.now()
        else:
            return dt.datetime.strptime(pickup_at, '%Y-%m-%dT%H:%M:%S')

    def _set_pu_tw_end(self):
        """
        From the pickup_at value add 15 minutes

        :return: set PU start / end TW
        """
        self.pu_tw['end'] = self.pu_tw['start'] + dt.timedelta(minutes=self.PU_TW_LENGTH)

    def _set_do_tw_end(self):
        """
        From the pickup_at value add 30 minutes

        :return: set PU start / end TW
        """
        self.do_tw['end'] = self.do_tw['start'] + dt.timedelta(minutes=self.DO_TW_LENGTH)

class Driver:
    def __init__(self, driver):
        for key in driver:
            setattr(self, key, driver[key])


class ProblemStatement:
    def __init__(self, ps):
        self.nb_jobs = len(ps['jobs'])
        self.nb_drivers = len(ps['drivers'])
        self.jobs = [Job(j) for j in ps['jobs']]
        self.drivers = [Driver(d) for d in ps['drivers']]

    def display_drivers(self):
        for driver in self.drivers:
            pp.pprint(driver.__dict__)

    def display_jobs(self):
        for job in self.jobs:
            pp.pprint(job.__dict__)


class CostFunction:
    invitationRetryCost = 1
    pickupWaitingTime = 250
    dropoffWaitingTime = 190
    timeToPUMean = 300
    searchingTimeMean = 60
    lateArrivalSlope = 0.05  # Factor that modifies the late arrival cost on routes
    scheduledSearchingTime = 900 # Seconds before a scheduled job is considered by the solver

    clientTiers = {
        'bronze': 2,
        'silver': 4,
        'gold': 6,
        'diamond': 8
    }

    def get_matrix(self):
        return np.zeros((self.ps_drivers, self.ps_jobs))

    def get_cost_invitation_retry(self, driver):
        """
        Computes the invitation try component cost of a driver

        :param driver: Driver object
        :return: float corresponding to cost
        """
        return self.invitationRetryCost * driver.expired_invitations[0]  # may fail if list empty

    def get_cost_driver(self, driver):
        """
        Compute the cost component (searching, lateness risk) of a driver

        :param driver: Driver object
        :return: float corresponding to cost
        """

    def get_cost(self, driver):
        cost_invitation_retry = self.get_cost_invitation_retry(driver)


def load_data():
    return json.load(open('data.json'))


if __name__ == '__main__':
    """
    The user creating the simulation gives the actual time he wants the dispatcher to start searching for
    drivers. The default value is set to 15 minutes as in the dispatcher reference if there is any scheduled job.
    
    NB: 1 km aerial distance = 1.3 km real distance.
    """
    # Load the ProblemStatement object
    data = load_data()
    ps = ProblemStatement(data)

    ps.display_drivers()
    ps.display_jobs()

    cost = CostFunction()
    cost.set_cost(ps)
    # m = cost.get_matrix()
    # print(m)
