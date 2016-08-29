#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

. /storage/.cache/services/diseqc.conf

VDR_LNBS="$LNB1 $LNB2 $LNB3 $LNB4"
lbn_k=1
k=0

  for lnbs in $VDR_LNBS; do
      eval LNB_S=\$LNB$lbn_k
      eval SAT_S=\$SAT$lbn_k
      [ "$SAT_S" != "none" ] && SAT_S=$(echo $SAT_S | awk '{print $1}')
      eval POLAR_S=\$POLAR$lbn_k

      if [ "$LNB_S" = "1" ] && [ "$SAT_S" != "none" ]; then

              if [ "$POLAR_S" = "Linear" ]; then
                  echo "# LNB-$lbn_k SAT: $SAT_S"
                  printf "%s 11700 V 9750 t v W15 [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 v W15 t\n" $SAT_S $(expr $k \* 4) $(expr $k \* 4) $(expr $k \* 4)
                  printf "%s 99999 V 10600 t v W15 [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 v W15 T\n" $SAT_S $(expr $k \* 4 + 1) $(expr $k \* 4 + 1) $(expr $k \* 4 + 1)
                  printf "%s 11700 H 9750 t V W15 [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 V W15 t\n" $SAT_S $(expr $k \* 4 + 2) $(expr $k \* 4 + 2) $(expr $k \* 4 + 2)
                  printf "%s 99999 H 10600 t V W15 [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 V W15 T\n" $SAT_S $(expr $k \* 4 + 3) $(expr $k \* 4 + 3) $(expr $k \* 4 + 3)
                  echo ""
              else
                  echo "# LNB-$lbn_k SAT: $SAT_S"
                  printf "%s 00000 R 10750 t v W15 [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 v W15 t\n" $SAT_S $(expr $k \* 4) $(expr $k \* 4) $(expr $k \* 4)
                  printf "%s 99999 R 10750 t v W15 [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 V [E0 10 38 F%X] W15 v W15 T\n" $SAT_S $(expr $k \* 4 + 1) $(expr $k \* 4 + 1) $(expr $k \* 4 + 1)
                  printf "%s 00000 L 10750 t V W15 [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 V W15 t\n" $SAT_S $(expr $k \* 4 + 2) $(expr $k \* 4 + 2) $(expr $k \* 4 + 2)
                  printf "%s 99999 L 10750 t V W15 [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 v [E0 10 38 F%X] W15 V W15 T\n" $SAT_S $(expr $k \* 4 + 3) $(expr $k \* 4 + 3) $(expr $k \* 4 + 3)
                  echo ""
              fi
      fi
      k=$(expr $k + 1 )
      lbn_k=$(expr $lbn_k + 1 )
  done
