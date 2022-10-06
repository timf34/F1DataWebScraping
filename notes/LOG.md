### 5/10/22

- Plan for today:
- [ ] Convert current data structure to be the same structure as we have with the normal F1 dataset.
  - Note that going forward I might want to change the datastructure that we use, so keep this in mind.
  - Note: I will keep working notes on Notion log to avoid it getting too messy in here. 

- Notes:
  - We now have our data in largely the same format as in the OG dataset (one long list, each car separated by a "\n")
    - Note: we might want to consider saving the data from Okayama for use in the future.
    - Added code to send our data to MQTT topics...
      - The size of the data is 9000 bytes currently in list format, which is too large! 
      - We should be able to send all the strings (names, etc.) at once initially. 

### 1/10/22

- Code for continous updates from the super taikyu website is together
- Code for pulling info from static website for the Timing Table is together

TODO next:

- [ ] Cleanup the code; write down a plan for what the structure should be like 
- [ ] Plan for testing the code that continuously pulls updates from the website. My sense is to run the html on a local server and then run code that updates the website.
- [ ] I should write notes down on HTML and CSS

- [ ] Not directly related to this project but I should start building websites/ web apps/ interfaces as some good practice.