import random
import threading

from proglog import ProgressBarLogger, TqdmProgressBarLogger

import user_interface


class MyBarLogger(TqdmProgressBarLogger):

    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))
            self.percentage_value = 0.0

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage = round((value / self.bars[bar]['total']) * 100, 1)
        # print(bar, attr, percentage)

        if user_interface.Interface.old_value != percentage:
            if percentage >= 99.9:
                percentage = 100.0
            user_interface.Interface.old_value = percentage
            user_interface.Interface.progress_bar_queue.put(percentage)

        # print(user_interface.Interface.old_value)
