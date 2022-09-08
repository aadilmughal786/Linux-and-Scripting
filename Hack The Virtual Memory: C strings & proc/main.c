#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/**
 * main - uses strdup to create a new string, and prints the
 * address of the new duplcated string
 *
 * Return: EXIT_FAILURE if malloc failed. Otherwise EXIT_SUCCESS
 */

int main(int argc, char const *argv[]){
    char* s;
    unsigned long int i;
    s = strdup("AadilMugal");
    if(!s){
    	fprintf(stderr,"Error while allocate memory.\n");
    	return (EXIT_FAILURE);
    }
    i = 0;
    while(s){
    	printf("[%lu] %s (%p)\n",i,s,(void*)s);
    	sleep(1);
    	i++;
    }
    return (EXIT_SUCCESS);
}