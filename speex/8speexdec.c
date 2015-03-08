#include <speex/speex.h>
#include <stdio.h>

/*The frame size in hardcoded for this sample code but it doesn't have to be*/
#define FRAME_SIZE 160
int main(int argc, char **argv)
{
   char *inFile;
   char *outFile;
   FILE *fout;
   FILE *fin;
   /*Holds the audio that will be written to file (16 bits per sample)*/
   char out[FRAME_SIZE];
   /*Speex handle samples as float, so we need an array of floats*/
   float output[FRAME_SIZE];
   //short in[FRAME_SIZE];
   char cbits[200];
   int nbBytes;
   /*Holds the state of the decoder*/
   void *state;
   /*Holds bits so they can be read and written to by the Speex routines*/
   SpeexBits bits;
   int i, tmp;

   /*Create a new decoder state in narrowband mode*/
   state = speex_decoder_init(&speex_nb_mode);

   /*Set the perceptual enhancement on*/
   tmp=1;
   speex_decoder_ctl(state, SPEEX_SET_ENH, &tmp);

   inFile = argv[1];
   outFile = argv[2];
   fin = fopen(inFile, "r");
   fout = fopen(outFile, "w");

   /*Initialization of the structure that holds the bits*/
   speex_bits_init(&bits);
   while (1)
   {
      fread(&nbBytes, sizeof(int), 1, fin);
      fprintf (stderr, "nbBytes: %d\n", nbBytes);
      if (feof(fin))
         break;
      
      /*Read the "packet" encoded by sampleenc*/
      fread(cbits, 1, nbBytes, fin);
      //fread(cbits, 1, nbBytes, stdin);
      /*Copy the data into the bit-stream struct*/
      speex_bits_read_from(&bits, cbits, nbBytes);

      /*Decode the data*/
      speex_decode(state, &bits, output);

      /*Copy from float to short (8 bits) for output*/
      for (i=0;i<FRAME_SIZE;i++)
         out[i]=output[i];

      /*Write the decoded audio to file*/
      fwrite(out, sizeof(char), FRAME_SIZE, fout);
   }
   
   /*Destroy the decoder state*/
   speex_decoder_destroy(state);
   /*Destroy the bit-stream truct*/
   speex_bits_destroy(&bits);
   fclose(fout);
   fclose(fin);
   return 0;
}
