/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>

#include "dictionary.h"

/**
 * Returns true if word is in dictionary else false.
*/

typedef struct node
{
char word[LENGTH+1];
struct node *next;
}
node;

node *hashtable[HASHTABLE_SIZE];
unsigned int word_count=0;
bool dictionary_loaded = false;

unsigned int hashword(const char *s)
{
    unsigned int hash = 0;
    for (int i = 0 ; s[i] != '\0' ; i++)
    {
        hash = 31*hash + s[i];
    }
    return hash % HASHTABLE_SIZE;

    /*
    unsigned int h;
    unsigned const char *us;
    us = (unsigned const char *) s;
    h = 0;
    while(*us != '\0')
    {
        h = h * MULTIPLIER + *us;
        us++;
    }
    return h;*/
}

bool check(const char *word)
{
    int len = strlen(word);
    char tempword[len+1];
    for(int i=0;i<len ;i++)
    {
        tempword[i] = tolower(word[i]);
    }
    tempword[len] = '\0';

    unsigned int hash = hashword(tempword);
    node* head = hashtable[hash];
    if(head==NULL)
    {
        return false;
    }
    else
    {
        while(head != NULL)
        {
            if (strcmp(head->word, tempword) == 0)
                return true;
            else
                head = head->next;
        }
        return false;
    }
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    char word[LENGTH+1]="";
    for(int i=0;i<HASHTABLE_SIZE;i++)
    {
        hashtable[i] = NULL;
    }

    FILE* fp = fopen(dictionary, "r");
    if (fp == NULL)
        return false;

    while(fscanf(fp,"%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if(new_node==NULL)
        {
            unload();
            return false;
        }
        strcpy(new_node->word, word);
        new_node->next = NULL;
        unsigned int hash = hashword(word);

        node* head = hashtable[hash];
        if(head==NULL)
        {
            hashtable[hash]= new_node;
        }
        else
        {
            new_node->next = head;
            hashtable[hash] = new_node;
        }
        word_count++;
    }
    fclose(fp);
    dictionary_loaded = true;
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if(dictionary_loaded)
        return word_count;
    return 0;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for(int i=0;i<HASHTABLE_SIZE;i++)
    {
        node* tempNode = hashtable[i];
        while(tempNode != NULL)
        {
            node* cursor = tempNode;
            tempNode = cursor->next;
            free(cursor);
        }
    }
    return true;
}
