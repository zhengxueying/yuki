#!/usr/bin/env python
#  -*- coding: utf-8 -*-'

import click

class TestClick():
    def cli(self,name):
        click.echo('test for setup %s'% name)
    def justforfun(self,fun):
        click.echo('funfunfunfun:%s'% fun)

@click.command()
@click.option("--name")
def cli(name):
    TestClick().cli(name)

@click.command()
@click.option("--fun")
def fun(fun):
    TestClick().justforfun(fun)

# if __name__ == '__main__':
#     cli()