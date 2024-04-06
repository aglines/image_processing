# image_processing
- I play around sometimes with AI image generation, and I even create my own models. Sometimes I want to publish these or send them out
- But I process them first: sometimes the images are of my family or myself, or I don't want them used to train another AI
- This code does some of these steps to save time

# DONE
- apply a watermark to an image
- apply partially-transparent watermark to an image
- replace filename with a UUID (version 4)
- batch process files in a directory
- detects image dimensions & applies correctly sized watermark
- watermarked copy erases metadata
- watermarked copy saved to a diff folder for other processing (TBD)
- basic exception handling

# TO DO
- logging
- save dimensions along with saved filename
- some formal tests
- save metadata of each file somewhere so I can keep track of the prompt used to create it

# Wish list
- Change UUID version to generate same UUID from same text (not nec, but in case of future data loss, can get metadata back from uuid)
- Create a QR code with more metadata (creation date, where published to, osv)
- Automate using Nightshade to render images less usable for other AI

# Project notes
## Switched to using python Pillow from Gimp's Python-fu. Why?
- Gimp Python-fu still only uses 2.7 (afaict) - so uhh... the next line is obvious
- Pillow == better, more, & newer documentation, larger active community etc etc
