![ECHO](https://github.com/user-attachments/assets/2e313394-b87c-4e16-99ba-69796744d9ef)

![Badge Development](https://img.shields.io/badge/STATUS-%20Development-green)
![Last Updated](https://img.shields.io/badge/Last%20Updated-April-blue)

## 📚 Table of Contents

- [🔊 What is Echo?](#-what-is-echo)
- [❓ Why Echo?](#-why-echo)
- [🚀 What does Echo do?](#-what-does-echo-do)
- [💡 Design Vision](#-desing-vision)
- [✨ User Interfaces Description](#-user-interfaces-description)
- [🚀 List of Project Functions](#-list-of-project-functions)
- [🌙 Moonshot Features](#moonshot)
- [👥 Authors](#-authors)
- [📄 Documentation](#documentation)
- [🧩 External Tools Used](#external-tools-used-)
- [🛠️ Tools and Technologies](#tools-and-technologies)
- [📦 Getting Started](#getting-started)


##  🔊 What is echo?

A web application is proposed for the evaluation and feedback of pronunciation of passive English speakers between 18 and 30 years old, using audio recordings of the speaker emulating audios and transcriptions in English used as didactic material. It will be developed as a web application, will make use of different artificial intelligence models to evaluate the audios and will store the didactic material and user information in a database.

## ❓ Why echo? 
Nowadays, mastery of the English language has become essential to have better social and work opportunities. The project seeks to attack the problem in which thousands of people find themselves, which is to learn to pronounce well, so the passive speaker will be able to use this tool to improve in the language and discover their weaknesses 

## 🚀 What does echo do? 
A web application is proposed for the evaluation and feedback of pronunciation of passive English speakers between 18 and 30 years old, using audio recordings of the speaker emulating audios and transcriptions in English used as didactic material. It will be developed as a web application, will make use of different artificial intelligence models to evaluate the audios and will store the didactic material and user information in a database.

## 💡 Desing Vision?
![Echo should look like a user-friendly, educational website.](https://github.com/user-attachments/assets/23378af0-6fea-4503-9528-888496f9d2ed)

**Echo should look like a user-friendly, educational website.**

## ✨ User Interfaces description
The system offers different user interfaces.


- Show an interface with all the resources available in the system divided by usage situation and subdivided by difficulty.
- Display an interface with a report of the user's progress and progress.
- Display an interface so that the user can request or enter generated texts.
- Display an interface to edit the user's profile.
- Show an interface for login.
- Display a user guide interface.

## 🚀 List of Project Functions
- `Functionality` 🎧 Provide audios and transcriptions of words, sentences, and texts as teaching materials.
- `Functionality` 🎙️ Allow the user to create audio recordings of the teaching material.
- `Functionality` 🤖 Provide AI feedback on the user's pronunciation.
- `Functionality` 🧠 Filter words, sentences, and texts by difficulty level.
- `Functionality` 🔍 Filter words, sentences and texts by usage situation.

### Moonshot:
* Generate audios and transcriptions using AI from a free request from the user on any topic.
* Generate audios and transcriptions using AI from text manually entered by the user.
* Allow the exchange between users of messages translated into English and their audios to receive feedback.

## 👥 Authors

- 👩🏻‍💻 [Valeria González Segura](https://github.com/valeria-gonzalez)
- 🧑🏽‍💻 [Diego Tristán Domínguez Dueñas](https://github.com/DiegoDominguez25)
- 🧑🏽‍💻 [Alan Josafat Ramos Preciado](https://github.com/Alan-codigo)

## Documentation

- [Documentation](https://docs.google.com/document/d/1B9YQfvb7I7E13JZI4Byv3aVxBOVHXdGzn8iEgpIhnzM/edit?tab=t.0)
- [Resourses](https://docs.google.com/document/d/1Et9c0ZzpGofkerB-mC5LdGqCwqHUKcXjMGOmZ4DnOt0/edit?tab=t.0)

## External Tools Used 🧩

### *Wikiextract*
### *Tatoeba*

## Tools And Technologies

### Front-End
- React
- JavaScript

### Back-end
- FastAPI

### Database
- Firebase



## Getting Started

### 📌 1. Locate your issue.
Navigate to the `Issues` tab and locate the issue you have been assigned.

### 🔧 2. Update its status and create your branch.
Change the issue's status to let others know you're working on it. Also create your branch to start with your local development. You can create a branch directly in the lower right corner of the page. 

🖥️ If you are creating your branch from your terminal, just remember to:

1. Make sure your situated at the main branch with `git checkout main`.
2. Update your main branch with `git fetch origin`.
3. Create your branch as `git checkout -b your_branch`.

   3.1 Name your branch with the following convention `IssueNumber-description-of-issue`. Example: `2-process-words`

If you created your branch from github, use the following to make sure you're where you need to be:

```
git checkout main
git fetch origin
git checkout your_branch
git branch
```

### 🗂️ 3. Save all data to a folder named dataset
Please save all of your data (such as .csv, .zip files) that aren't directly related to the data processing scripts in a folder named `datasets`. The `.gitignore` file will ignore it no matter where it is.

If you are creating a virtual environment for python (which is recommended), please name it `env` so it's ignored as well.

If you are creating any other folder that isn't relevant to all of us, kindly add it to the `.gitignore` file and update it here so we're all aware of the changes.

```
env
**/datasets/*
```
