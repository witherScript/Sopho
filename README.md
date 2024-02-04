## Name of Student 
Genesis Scott

## Name of Project
InterKnowing

## Project's Purpose or Goal (What will it do for users?)

This project will provide users with a platform to create a learning path for any topic, generate learning resources organically, and display a visual relationship between related subtopics. Ultimately, the user will be able to visually follow their own progress to subject mastery, modeling cutting edge teaching strategies that involve research around:
  - Spaced Repetition to ensure long-term retention
  - Anki-style Active Recall
  - Bloom's Taxonomy


## List the absolute minimum features the project requires to meet this purpose or goal

- Landing view that visually explores the site and what users can expect out of it
- Authentication and Authorization - firestore or other (saves user info, learning path information)
- An optimized knowledge query service that takes a string topic as input and outputs a tree of related subtopics **optimally** (could use Selenium or something else - but building with scale in mind: would be more inexpensive to cache related subqueries ex: someone wants to learn "Java" -> Sub-topics related to Java mastery would be cached in future students' req for same term.) [-1]

## What tools, frameworks, libraries, APIs, modules and/or other resources (whatever is specific to your track, and your language) will you use to create this MVP? List them all here. Be specific.



### - Front-end in React [0]
  **subtopics**:
    - Landing page, potentially some of the UX as well but that may change as it develops. 
    - Input form for intaking a topic and related information
      - User will input: Topic title, maybe a few possible sub-groups of components during development (user would provide direct feedback to the knowledge engine by selecting a preferred roadmap)
### - "Knowledge Query" Service that creates a graph for a topic given an input - maybe a C# API that interfaces with a self-hosted NN written from the ground up in Python. [1]
   **subtopics**:
      - Neural Engine trained locally and hosted in one of Azure, AWS or Google Cloud (pending alternatives, could also host locally- TBD)
      -  Word embeddings: could store in a GraphQL database[2]
### - User data: firestore for encrypted account information
  **subtopics**:
    - application layer vs application data -> could

  Relevant: Personal Knowledge Management System: https://able.ac/blog/personal-knowledge-management/

  Ex:

  Java:
  - Syntax:
    - Loops
    - Variables
    - Conditionals

https://www.turing.ac.uk/research/interest-groups/knowledge-graphs

## If you finish developing the minimum viable product (MVP) with time to spare, what will you work on next? Describe these features here Be specific.


- Notification system for updates

Front-end:
  - fully integrated User experience - user's first visit takes them through an intro and tour of the tool, no clear redirect/refresh from landing on the site to navigating to a learning path. 

Backend/Knowledge layer:
  - caching Knowledge Query service to only use neural net when necessary rather than generating every query from scratch
  For each graph node:
  -  engine to parse learning data into modules and click-through lessons:
    - incremental reading support for articles
      - bionic reading for increasing comprehension
    - Anki-like flashcards 
    - Project prompts that have clear expectations and the capacity to give feedback, taken from scanning syllabus, textbooks, things that are classified as thematically "Relevant" to each node.
    - Focused vs diffused focus - Barbara Oakley 


## What additional tools, frameworks, libraries, APIs, or other resources will these additional features require?

- React Toastify could work for notifications - 
- Right now, the Neural Network is planned to be written with Python, Tensor flow



## Is there anything else you'd like your instructor to know?



#### Notes:
[-1]
[here](https://twitter.com/albera_com?lang=en) is an example of a similar service with a slightly different purpose

[0] might need to use something more simple and lightweight, like if I want the crux of the work to be done on the backend I could use HTMX and Go, which provide excellent support for templating Views, and could more natively accommodate input from Neural Network. Go has excellent support for threads and HTMX is lightweight compared to React. **Ryan:** let me know if it's cool with you for me to use a different language- none of this would've been possible without Epicodus)

[1] Might need functional language to better store abstract information. Real time data fetching for taking a text and processing it through some large-text search to infer related sub-topics. 
[2] See https://www.youtube.com/watch?v=21pJJ4J86zA


#### Side-Notes:
might do something inspired by [Natural Language Pre-processing](https://aws.amazon.com/what-is/nlp/#:~:text=Natural%20language%20processing%20(NLP)%20is,manipulate%2C%20and%20comprehend%20human%20language.) -  this field is concerned with computers interpreting text - prior to data intake, the strings are broken into tokens and optimized by removing stop-words and irrelevant terms. It would make sense to build a sort of - real-time data pipeline:
    input: the user's topic 
    output: graph/tree of relevant sub-topics (parent = abstract topic, subcomponent = partitions towards mastery)


Important: I need to think about exactly how "competence" is measured per topic. 

Practical experience in the form of projects.
Intake in the form of reading, some transcription
Progress report per arbitrary checkpoint in learning path
