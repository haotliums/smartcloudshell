import csv, json, os, yaml
from typing import List

import datetime
import modelFactory
# from Model import baselineModel_lg, baselineModel_sm
from modelBase import CliNlpModel
from measure.testset import TestCase, TestSet, testset_queries, testset_labeledqueries
from measure.testrunner import TestRunner, TestReportDiff, TestReport

def ensureTestRunerCanRun():
  runner = TestRunner(testset_queries, modelFactory.getModelWithAbbrQRAndSpeller_smdata_smmodel())
  report1 = runner.run()
  report1.saveToYamlFile()

def compare(testSet: TestSet, model1: CliNlpModel, model2: CliNlpModel):
  runner = TestRunner(testSet, model1)
  report1 = runner.run()
  report1.saveToYamlFile()

  runner = TestRunner(testSet, model2)
  report2 = runner.run()
  report2.saveToYamlFile()

  diff = TestReportDiff.diffReports(report1, report2)
  diff.saveToYamlFile()

def compareAzureResourceRecognizerModelVsBaseLine():
  compare(testset_queries, modelFactory.getModelWithAzureResourceRecognizer(), modelFactory.getBaselineModel())

def compareAbbrQrModelWithAndWithoutSpeller():
  compare(testset_labeledqueries, modelFactory.getModelWithAbbrQRAndSpeller(), modelFactory.getModelWithAbbrQR())

def compareWithAndWithoutStopsQr():
  compare(testset_labeledqueries,  modelFactory.getModelWithAbbrQrStopsQrAndSpeller(), modelFactory.getModelWithAbbrQRAndSpeller())

def compareReports(reportPath1: str, reportPath2: str):
  report1 = TestReport.loadFromYamlFile(reportPath1)
  report2 = TestReport.loadFromYamlFile(reportPath2)
  diff = TestReportDiff.diffReports(report1, report2)
  diff.saveToYamlFile()

# ensureTestRunerCanRun()
# compareAzureResourceRecognizerModelVsBaseLine()
compareWithAndWithoutStopsQr()

#compareReports('queries_lgd_lgm.report', 'queries_lgd_lgm_abbr.report')
# TODO: add more runner to measure different combinations
