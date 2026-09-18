

Questions i have:
- ROSIE gives me 50 channels, i am unsure of the channels, is the channels consistent? For example: Is channel 0 always DAPI?

- Overleaf Premium

- Image resoluiton. I run inference on the H&E image, i was wondering if the should have better resolution. I have cross referenced the papers and image file meta data, and i have concluded with it being fine.



- har det H&E bildet som jeg sendte inn flere enn 1 kanal? håper ikke det






1. X Finne ut hvordan jeg sender Wally bilde gjennom modellen
2. X Finne ut hvordan man setter opp prosjektet for Springfield
3. X Sette prosjektet opp for Springfield


4. X Teste om ROSIE faktisk fungerer (gir oss de 50 ish biomarkørene som er forventet at den skal gi)
 -  ROSIE gir oss 50 kanaler, er usikker på hva kanalene faktisk sier 


5. Dobbelt sjekke om kanalene er i riktig rekkefølge
    - Det kan hende at de har endret rekkefølgen til kanalene, men DAPI bør være den første kanalen. 
    - Hvis kanalene er i riktig rekkefølge, så må vi teste:
        1. om innstillingene er riktig i forhold til hva ROSIE forventer
        2. Evt. spørre om vi kan få tilgang til treningsdataen for å teste.


6. Lage et histogram med verdier fra 0-1?
7. X Til abstracten, lage et bilde som er sydd sammen av de tre bildene i "resized_IF" DAPI skal være blå, CD45 grønn og Ecad kan være rosa.
8. 



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


