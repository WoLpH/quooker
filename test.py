#!C:\Python25 python

from quooker.step.input.csv_input import CsvInput
from quooker.job.job import OfferJob
from itertools import islice
from pprint import pformat, pprint
from quooker.auto_configure.column_auto_configure import ColumnAutoConfigure

def preview(iterable):
    pprint( list(islice(iterable,0,4)) )
    
    
input = CsvInput(None, 'sample_data/modern.csv')
job = OfferJob('modern_offer_job', 158571)
steps = []
job.steps = steps
#job_output = job.execute(input, test=True)
sample = list(islice(input,0,4))
auto = ColumnAutoConfigure(sample)
pprint( sample )
print auto.auto_config()
print 'done'

