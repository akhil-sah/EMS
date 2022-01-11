# Environment Management System

[![GitHub Stars](https://img.shields.io/github/stars/akhil-sah/EMS.svg)](https://github.com/akhi-sah/EMS/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/akhil-sah/EMS.svg)](https://github.com/akhil-sah/EMS/issues)

An Environmental Management System (EMS) is a framework that helps an organization achieve its environmental goals through consistent review, evaluation, and improvement of its environmental performance.

## Table of contents

- [General Info](#general-info)
- [Screen Captures](#screen-captures)
  - [Home Page](#home-page)
  - [Login Page](#login-page)
  - [Register Page](#register-page)
  - [User Profile Page](#user-profile-page)
  - [Maximum Permissible Emission Page](#maximum-permissible-emission-page)
  - [Audit Emissions Page](#audit-emissions-page)
  - [Survey Page](#survey-page)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)

## General Info

An environmental management system (EMS) is a system and database which integrates procedures and processes for training of personnel, monitoring, summarizing, and reporting of specialized environmental performance information to internal and external stakeholders of a firm (Source: [Wikipedia](https://en.wikipedia.org/wiki/Environmental_management_system)). This tool aims at aiding an organization to achieve their environmental goals by helping the organization/company to ensure compliance with government guidelines and provide them with timely feedbacks from various stakholders.

## Screen Captures

Screen captures of some of the web pages of the website.

### Home Page

![Website Preview](./ss/Capture1.PNG)

### Login Page

![Website Preview](./ss/.png)

### Register Page

![Website Preview](./ss/.png)

### User Profile Page

![Website Preview](./ss/.png)

### Maximum Permissible Emission Page

This page displays the values of maximum permissible limits for various pollutants. The values should be as per the government’s guidelines (the picture shows just some sample values).

![Website Preview](./ss/.png)

### Audit Emissions Page

This page displays a collapsible list of all the sessions for entering company’s emissions. On clicking a session the details for that session is shown and a table with emission details is displayed. The pollutants within permissible limits are shown in green color while those out of range are marked with red color. 

![Website Preview](./ss/.png)

The auditor can update the values (after directing the company’s relevant authorities to take suitable actions to check the pollutants concentration) of emitted pollutants that are out of range.

![Website Preview](./ss/.png)

### Survey Page

This page displays a list of surveys conducted by the company. Each content of list directs the surveyor to a page to accept response of a survey participant of that survey.

![Website Preview](./ss/.png)

## Features

- Code collaboration at real time
- Support for multiple programming language syntax
- Support for multiple editor background themes
- Realtime communication via audio and video chat
- Upload/Download source code
- Text reader for reading content of editor
- Supports multiple users (tested upto 10 users)

## Frameworks and libraries

- Django - version 3.2.7
- Crispy-forms - version 1.13.0
- Bootstrap - version 4.0.0

## Setup

(The various commands are for windows OS)
- The system should have [python](https://www.python.org/downloads/) installed on it as the website was built using django which is python web framework.
- Create virtual environment in python using the command given below (recommended to avoid future compatibility issue due to different versions)
  - To install virtualenv package
  ```sh
  pip install virtualenv
  ```
  - To create virtualenv
  ```sh
  python -m venv env_name
  ```
  - To activate the virtual environment, navigate to directory created by virtualenv, then use the command
  ```sh
  scripts\activate
  ```
- Install django (the website was built using version 3.2.7)
```sh
pip install Django==3.2.7
```
- Install cripy-form module
```sh
pip install crispy==1.13.0
```
- The website also sends mail to it's users and to enable that feature an email host should be provided. For that navigate to EnvManSys directory and in the settings.py file add the email account and it's password as shown below
```sh
EMAIL_HOST_USER = 'samplemail@abc.com'
EMAIL_HOST_PASSWORD = 'samplepassowrd'
```
