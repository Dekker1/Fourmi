# Fourmi

Fourmi is an web scraper for chemical substances. The program is designed to be
used as a search engine to search multiple chemical databases for a specific
substance. The program will produce all available attributes of the substance
and conditions associated with the attributes. Fourmi also attempts to estimate
the reliability of each data point to assist the user in deciding which data
should be used.

The Fourmi project is open source project licensed under the MIT license. Feel
free to contribute!

Fourmi is based on the [Scrapy framework](http://scrapy.org/), an open source
web scraping framework for python. Most of the functionality of this project can
be traced to this framework. Should the documentation for this application fall
short, we suggest you take a close look at the [Scrapy architecture]
(http://doc.scrapy.org/en/latest/topics/architecture.html) and the [Scrapy
documentation](http://doc.scrapy.org/en/latest/index.html).

### Installing 

If you're installing Fourmi, please take a look at our [installation guide](...)
on our wiki. When you've installed the application, make sure to check our
[usage guide](...).

### Using the Source

To use the Fourmi source code multiple dependencies are required. Take a look at
the [wiki page](...) on using the application source code for a step by step
installation guide.

When developing for the Fourmi project keep in mind that code readability is a
must. To maintain the readability, code should be conform with the
[PEP-8](http://legacy.python.org/dev/peps/pep-0008/) style guide for Python
code. More information about the different structures and principles of the
Fourmi application can be found on our [wiki](...).

### To Do

The Fourmi project has the following goals for the nearby future:

__Main goals:__

- Improve our documentation and guides. (Assignee: Dekker)
- Build an graphical user interface(GUI) as alternative for the command line
interface(CLI). (Assignee: Harmen)
- Compiling the source into an windows executable. (Assignee: Bas)
- Create an configuration file to hold logins and API keys.
- Determine reliability of our data point.
- Create an module to gather data from NIST. (Assignee: Rob)
- Create an module to gather data from PubChem. (Assignee: Rob)

__Side goals:__

- Clean and unify data.
- Extensive reliability analysis using statistical tests.
- Test data with Descartes 1.

### Project Origin

The Fourmi project was started in February of 2014 as part of a software
engineering course at the Radboud University for students studying Computer
Science, Information Science or Artificial Intelligence. Students participate in
a real software development project as part of the
[Giphouse](http://www.giphouse.nl/).

This particular project was started on behalf of Ivo B. Rietveld. As a chemist
he was in need of an application to automatically search information on chemical
substances and create an phase diagram. The so called "Descrates" project was
split into two teams each creating a different application that has part of the
functionality. We are the team Descartes 2 and as we were responsible for
creating a web crawler, we've named our application Fourmi (Englis: Ants).

The following people were part of the original team:

- [Jip J. Dekker](http://jip.dekker.li)
- Rob ten Berge
- Harmen Prins
- Bas van Berkel
- Nout van Deijck
- Michail Kuznetcov