#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:LaunchJobService.py
@time:2022/03/21
"""
from app import App
from repository.LaunchJobRepository import LaunchJobRepository, LaunchJobDetailRepository
from repository.ProjectRepository import ProjectRepository
from repository.ProductlineRepository import ProductLineRepository
from repository.WorkerRepository import WorkerRepository


class LaunchJobService:

    def __init__(self):
        pass

    def add(self, launchJob):
        cur_session = App().db.create_scoped_session()
        with LaunchJobRepository(cur_session) as ljr, LaunchJobDetailRepository(cur_session) as ljdr:
            ljr.add(launchJob)
            for launchJobDetail in launchJob.launchJobDetail:
                launchJobDetail.job_id = launchJob.id
                ljdr.add(launchJobDetail)

    def query(self, pageSize: int, currentPage: int, condition: dict):
        cur_session = App().db.create_scoped_session()
        with ProjectRepository() as pr, ProductLineRepository(cur_session) as plr, LaunchJobRepository(
                cur_session) as ljr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            # condition['deleted'] = 0
            projects = pr.listAll(dict(deleted=0))
            # 查询所有生产线，这里不过滤已删除的，因为已删除的生产线曾今可能运行过
            productlines = plr.listAll({})
            total = len(ljr.listAll({}))
            launchJob = ljr.listPage(start, end, condition)
            for job in launchJob:
                tmpProductline = list(filter(lambda productline: productline.id == job.productline_id, productlines))[0]
                tmpProject = list(filter(lambda project: project.id == tmpProductline.project_id, projects))[0]
                job.productLine = tmpProductline
                job.project = tmpProject
            return total, launchJob

    def queryDetail(self, launchJobId: int):
        cur_session = App().db.create_scoped_session()
        with LaunchJobDetailRepository(cur_session) as ljdr, WorkerRepository(cur_session) as wr:
            # 这里查询所有worker,不过滤已删除的工人，有些工人和生产线可能已经被删除但历史执行过
            workers = wr.listAll({})
            details = ljdr.getDetail(launchJobId)
            for detail in details:
                tmpWorker = list(filter(lambda w: w.id == detail.worker_id, workers))[0]
                detail.work = tmpWorker
        return details


if __name__ == '__main__':
    pass
