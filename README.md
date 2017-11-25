# Tutoria
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
[![Build Status](https://travis-ci.com/li-boxuan/tutoria.svg?token=9cK4Kmeqpdioyfb1EXxS&branch=master)](https://travis-ci.com/li-boxuan/tutoria)
[![Chat on Gitter](https://badges.gitter.im/Hola-Inc/Tutoriac.svg)](https://gitter.im/Hola-Inc/Tutoria)

![Hola the Monkey](./favicon/hola.png)

**You just found Tutoria.**

Tutoria is a university-based professional online platform for regular and private
campus tutoring that seamlessly supports
easy management of booking and sharing feedback. Latest technologies
are incorporated for granting state-of-the-art user experience.

Tutoria is proudly powered by [Django](https://www.djangoproject.com/)<sup>®</sup>.

## Installation

Before installation, you should have a working `django` copy. To obtain one,
you may visit [Django's website](https://www.djangoproject.com/).

First, clone this repo using `git`:

    git clone https://github.com/li-boxuan/tutoria.git

Then migrate the models. We provide a `Makefile` for automating
this process. To make a clean build, issue

    cd tutoria && make rebuild_empty

Or you can populate some demo data:

    cd tutoria && make rebuild
    
Afterwards, you can runserver and launch the application
via `localhost`:

    python manage.py runserver


## Development

[Jinyu Cai](https://www.linkedin.com/in/金雨-蔡-170b75108)<sup>&ast;</sup>,
[Boxuan Li](https://li-boxuan.github.io/)<sup>&ast;</sup>,
[Jiayao Zhang](https://i.cs.hku.hk/~jyzhang/)<sup>&ast;</sup> and
[Jingran Zhou](https://jrchow.github.io/)<sup>&ast;</sup>

<sup>&ast;</sup>The contributors are with the
[Department of Computer Science](https://www.cs.hku.hk/),
[The University of Hong Kong](https://www.hku.hk/), equally contributed.

## Acknowledgment

The contributors to this project wish to thank
[Mr. George Mitcheson](http://www.cs.hku.hk/people/profile.jsp?teacher=georgem)
for his generous help and advice throughout this project.

## Cite this Project

    @misc{tutoria:2017,
        title = {Tutoria},
        year = {2017},
        author = {Cai, Jinyu* and Li, Boxuan* and Zhang, Jiayao* and Zhou, Jingran*},
        publisher = {GitHub},
        journal = {GitHub Repository},
        howpublished= {\url{https://github.com/li-boxuan/tutoria}}
    }
    
 ## Disclaimer
 
 This project has been submitted for partial fulfillment for the course *Software Engineering* offered by Unversity of Hong Kong, 2017-18.

