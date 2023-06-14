# Tetun Crawler Pipeline


## Overview

Tetun crawler pipeline is a data collection pipeline designed for low-resource languages and built on top of Nutch and incorporating language-specific components such as a tokenizer and a language identification model.


## Requirements

### Technical
- [ ] Apache Nutch.
- [ ] Apache Solr.

### Language-specific
- [ ] An initial text corpus containing the target language.
- [ ] A tokenizer.
- [ ] A language identification model.


## Getting started

**Note:** The following commands are intended for the Ubuntu Linux environment.

- [ ] Create a project folder named `crawler-home`.

```
$ mkdir crawler-home
```

- [ ] Navigate into the project folder and install `pip`, create a virtual environment (here we use `pipenv`), and activate it:

```
$ cd crawler-home
$ sudo apt install python3-pip
$ pip install pipenv
$ pipenv shell
```

- [ ] Install `git` and clone the source code of the pipeline:

```
$ sudo apt install git
$ git clone https://github.com/borulilitimornews/crawler-pipeline.git
```

## Setting up Apache Nutch and Solr

To set up Apache Nutch and Solr, follow these steps:

- [ ] **Download Apache Nutch and Solr:** download the Apache Nutch and Solr packages and save them to the **crawler-home** directory. Ensure that you download the appropriate versions compatible with your system.

- [ ] **Configure Apache Nutch:** refer to the [Nutch installation and configuration tutorial](https://cwiki.apache.org/confluence/display/NUTCH/NutchTutorial) for detailed instructions on configuring Nutch. Follow the tutorial, but skip the **Crawl your first website** section and proceed directly to the **Setup Solr for search** section.

- [ ] **Rename the Nutch and Solr packages:** after downloading the packages, rename the Nutch package directory from `apache-nutch-1.x` to `nutch` and the Solr package directory from `apache-solr-9.x` to `solr`.

- [ ] **Verify the Nutch and Solr configuration:** after completing the configuration steps, verify that both Nutch and Solr are working correctly. You can do this by following the verification steps provided in the tutorial.


## Setting up the pipeline

To set up the pipeline, you will need to organize the following main folders in the specified structure:

- [ ] **bin**: this folder contains a bash file that allows configuration of seeder iterations and crawling rounds.
- [ ] **pipeline**: this folder contains include the codes for the seeder, corpus construction, and corpus summary generation. It also contains the LID model, data, and log folders.
- [ ] **nutch**: it contains the Nucth framework files.
- [ ] **solr**: it contains the Solr framework files.


### Create folders and copy the LID model and initial corpus

Create the LID, data, and log folders within the pipeline folder. 

```
$ cd pipeline
$ mkdir data lid log
```

Copy the LID model, name it `lid_model.pkl`, and locate it in the **lid** folder. 

```
$ cp {PATH_TO_THE_LID_FILE} ./lid/
```

Copy the initial corpus, name it `initial_corpus.txt`, and locate it in the **data** folder.

```
$ cp {PATH_TO_THE_INITIAL_CORPUS_FILE} ./data/
```

Replace **{PATH_TO_THE_LID_FILE}** and **{PATH_TO_THE_INITIAL_CORPUS_FILE}** with the actual path to the LID model and the initial corpus files you want to copy. 


`[Optional]`

If you want to use the module to generate a data sample for evaluation purposes, you can create an additional folder inside the **data directory** and name it `evaluation_sample`. This folder will be used to store the generated data sample.


### Configuration module

In the configuration module, you will find the general pipeline configuration located in **pipeline/common_utils/config.py**. This configuration module consists of the following components:

- [ ] **File paths:** This section contains the paths to various files that are either required by the pipeline or will be generated by the pipeline.
- [ ] **Solr:** The Solr configuration is included in this section. It is recommended to keep this part unchanged unless necessary.

- [ ] **Language, LID model, and corpus:** The configuration in this group and the following sections can be adjusted according to your specific requirements. This includes settings related to language processing, the Language Identification (LID) model, and the corpus used by the pipeline.


### Configure the LID model

To configure the Language Identification (LID) model in the pipeline, follow these steps:

- [ ] Open the file **pipeline/common_utils/tetun_lid.py**.
- [ ] Locate the `get_tetun_text`function within the file.
- [ ] Adjust the function according to the nature of your LID model.
- [ ] **Ensure that the function receives a list of strings as input.** This is important for optimizing the corpus construction process and making it faster. Make the necessary modifications to the `get_tetun_text` function based on your LID model's requirements.


## Execute the pipeline

To execute the pipeline and initiate the crawling process, follow these steps:

- [ ] On the `crawler-home` directory, run the bash file named `crawler.sh`using the following command:

```
$ bash ./bin/crawler.sh
```

Running this command will execute the pipeline and automatically start the crawling process. Please ensure that you are in the correct directory before executing the command, as the path `./bin/crawler.sh` should be relative to the current working directory.
