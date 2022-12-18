### Pitch Diagrammer

This repo contains a python script to generate pitch accent diagrams for languages like Japanese or Korean.  It comes with several command-line options for setting things like size parameters, the desired word, and the desired pitch pattern.

Examples: 
- `python3 draw.py --pitch_pattern LHLLH --text_string 감사합니다 --height 150 --step 100 --padding 10 --outer_point_radius 10 --inner_point_radius 8 --output_file example.svg`
- `python3 draw.py --pitch_pattern LHLLH --text_string 감사합니다`

### Resources
- https://seriot.ch/pycairo/#3_clip_and_mask.clip
- https://www.cairographics.org/cookbook/outside_clipping/

