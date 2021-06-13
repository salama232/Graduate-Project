if [ $(date +%M) != "00" ]; then date +%-H:%M%p%Z; else echo -n $(date +%-H); echo -n "oh clock "; date +%p; date +%Z; fi | espeak -g20 -ven+f6
