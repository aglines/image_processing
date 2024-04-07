# image_processing
- I play around sometimes with AI image generation. Sometimes I want to publish these or send them out
- But they need processing first: sometimes the images are personal, my family, etc, or I don't want them used to train another AI
- This code performs some of these steps, to save time

# DONE
- apply a watermark to an image
- apply partially-transparent watermark to an image
- replace filename with a UUID (version 4)
- batch process files in a directory
- detects image dimensions & applies correctly sized watermark
- watermarked copy erases metadata
- watermarked copy saved to a diff folder for other processing (TBD)
- basic exception handling
- better logging committed to logging branch: set levels, handles specific FileNotFound exception

# TO DO
- shorten basefile name to human-readable lengths (basefile name can incl prompt info which maxes out filename limits)
    - 11 char. 5 digits then hyphen then 10 digits. enough to ID visually
- save dimensions into saved filename
- some formal tests
- save metadata of each file somewhere so I can keep track of the prompt used to create it

# Wish list
- Change UUID version to generate same UUID from same text (not nec, but in case of future data loss, can get metadata back from uuid)
- Create a QR code with more metadata (creation date, where published to, osv)
- Automate using Nightshade to render images less usable for other AI

# Project notes
## Switched to using python Pillow from Gimp's Python-fu. Why?
- Gimp Python-fu still only uses 2.7 (afaict) - easier to work with modern tools
- Pillow: better, more, & newer documentation, larger active community etc
