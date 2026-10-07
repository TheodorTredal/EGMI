

Questions i have:
- ROSIE gives me 50 channels, i am unsure of the channels, is the channels consistent? For example: Is channel 0 always DAPI?

- Overleaf Premium

- Image resoluiton. I run inference on the H&E image, i was wondering if the should have better resolution. I have cross referenced the papers and image file meta data, and i have concluded with it being fine.



- har det H&E bildet som jeg sendte inn flere enn 1 kanal? håper ikke det






1. X Finne ut hvordan jeg sender Wally bilde gjennom modellen
2. X Finne ut hvordan man setter opp prosjektet for Springfield
3. X Sette prosjektet opp for Springfield
4. X Teste om ROSIE gir oss 50 forskjellige kanaler
5. X Dobbelt sjekke om kanalene er i riktig rekkefølge.
6. Sjekke om innstillingene er riktig i forhold til hva ROSIE forventer:
  -> Har bildet riktig oppløsning? Gjør dette en gang til.
  -> Bør vi istedenfor 8, kjøre 4 steps, eller 2?
    -> i Så fall så må jeg finne ut hvor mye bilde bør splittes med for å så sy det sammen senere.
  -> Evt. Spørre om tilgang til treningsdataen for å teste.
7. X Sende inn abstracten.
8. X Lage et histogram med verdier fra 0-1?, Må gjøres på nytt og skikkelig.
9. X Til abstracten, lage et bilde som er sydd sammen av de tre bildene i "resized_IF" DAPI skal være blå, CD45 grønn og Ecad kan være rosa. 
10. Zenodo bildet har flere pixeler per mikrometer enn det ROSIE forventer! Om bildet er tatt med 20X eller 40X har ingenting å si så lenge oppløsningen er riktig. Derfor kan det være feil å oppskalere (interpolere bildet), men heller downscale bildet istedenfor. Jeg skal derfor kjøre 2 nye tester:
  1. jeg tar et 3000x3000 sample av bildet og kjøre med de beste innstillingene.
  2. Jeg skal downsample bildet slik at det har akkurat de innstillingene ROSIE forventer (≈0.3775 μm/px) og kjøre det gjennom modellen med de beste innstillingene også her med et utsnitt på 3000x3000 px bilde.
  (N.B!) Har forresten brukt feil bilde. Bildet (czi.tif bildet) jeg brukte var en downsampla versjon av det ekte bildet som bare er en .czi fil. 



# MÅ JOBBE LITT ANNERLEDES
Testene tar for lang tid. Vi kutter ned bildet til 3000x3000 piksler i henhold til ROSIE artikkelen. Vi velger ut et interesse område og kjører forskjellige tester på det området for å se hva som må til for å få resultatene vi trenger.





HVA ER ZENODO FILEN SIN PX PER MICRO METER??






How to run
0. må bruke Cisco VPN for å logge på Springfield
1. Dockerfile + Docker image + Docker build
2. environment.yaml
3. job.yaml
4. X job script
5. Frink
5. 






POTENTIAL FIND:
According to the initial tests of ROSIE, if channel 0 is DAPI, then the model outputs widely different then what is expected. This might mean that ROSIE cannot generalize to images outside of the training data, most likely this is because the image has a slightly different resolution than what ROSIE expects, leading to hallusination.

The image sent into ROSIE were IMAGE 1: Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif



Trying to upscale the image (adding information that may not exist, need to read a bit more up on interpolation upscaling) to see if that may help on the inference part of the image. 

But first i am trying to run the code without excluding the background and without running post processing image 1, unlike the first inference run. 








INFO OM Zenodo bildet:

DoAutoScalingSynchronization: false
SelectedScalingMaster: LSM
TheoreticalTotalMagnification: 20
TotalMagnification: 20
DefaultScalingUnit: µm
TheoreticalTotalMagnification: 0.06195
TotalMagnification: 0.06195
DefaultScalingUnit: µm
TheoreticalTotalMagnification: 20
TotalMagnification: 20
DefaultScalingUnit: µm
TheoreticalTotalMagnification: 0.06195
TotalMagnification: 0.06195
DefaultScalingUnit: µm
TheoreticalTotalMagnification: 20
TotalMagnification: 20
DefaultScalingUnit: µm
TheoreticalTotalMagnification: 20
TotalMagnification: 20
DefaultScalingUnit: µm
Magnification: 0.06195
Magnification: 2.5
Magnification: 10
Magnification: 20
Magnification: 40
Magnification: 0
Magnification: 0
Magnification: 5
Magnification: 1
Magnification: 1
ImageScaling: 
      
ScalingComponent: None
ScalingComponent: None
ScalingComponent: None
ScalingComponent: None
ScalingComponent: None
ScalingComponent: None
ScalingComponent: None
NominalMagnification: 20
Scaling: 



(env) theodortredal@tromso-studenter1-3003 EGMI % /Users/theodortredal/Desktop/EGMI/env/bin/python /Users/theodortredal/Desktop/EGMI/python_scripts/crop_image.py
/Users/theodortredal/Desktop/EGMI/python_scripts/crop_image.py:104: DeprecationWarning: Testing an element's truth value will raise an exception in future versions.  Use specific 'len(elem)' or 'elem is not None' test instead.
value_node = elem.find("./Value") or elem.find(
Akse Ukjent: -2.00e-06 m/px (-2.0000 µm/px)
Akse Ukjent: 2.00e-06 m/px (2.0000 µm/px)
Akse Ukjent: 1.00e-06 m/px (1.0000 µm/px)
Akse X: 2.20e-07 m/px (0.2200 µm/px)
Akse Y: 2.20e-07 m/px (0.2200 µm/px)