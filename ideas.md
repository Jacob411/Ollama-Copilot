# Ideas for features/Improvements
- [ ] Explore more ollama features, such as generate and context
- [ ] limit when to offer multiline completion (middle of line) and also make it work with multi line smoothly
- [ ] add config options
- [ ] Improve when to trigger completion.
- [ ] Fix issue where completion keeps streaming after a change / cancel
- [ ] Need to update readme for more detailed instructions and Usage.
- [ ] Use a map of the file to store completion data, to avoid having to recompute it if user comes back to location. 
- [ ] Change triggers for completion to be more flexible, and allow for more customization. Currently activates on new words and on "." and " ".
- [x] Make ls into class, use did change as trigger to stop completion. Maybe through a check before sending each piee, or check to see which piece is change, if it fits the suggestion simply cut the front off and send the rest.
