# include <stdio.h>
# include <stdlib.h>
#include <time.h>
int main (){
    
    int table[100];
    int all[100];
    int g=0;
    srand(time(0));
	printf("                                                    who will get a promotion this year ?");
	for(int a=0;a<100;a++){
       table[a]=a+1;
      all[a]=(rand()% 100)+1 ;
      printf("\n\nEmployee %d: Has %d deals done",table[a],all[a]);
  
   if(all[a]>50) {
  
	g++;
}
}
 
  printf("\n\nThe number of employess with more than 50 deals done is: %d",g);

 
  printf("\n\nSo these %d employees shall get a promotion plus a 1000dhs bonus.",g);
 printf("\nThanks everyone for your efforts!");
   return 0;
}