# Terminapy

Terminapy is a library use for display a basic ascii / Unicode screen on the terminal

## What is this Lib
This lib is a Class "**screen**" that help you do display screen on the terminal like:
```plaintext
╭───────────────────────┬───────────────────────╮
│                       │                       │
│                       │                       │
│                       │                       │
│                       │                       │
│                       │                       │
│                       │                       │
│                       │                       │
│                       │                       │
│ Display Text          │ Display Text 2        │
╰───────────────────────┴───────────────────────╯
```

It is base on the princip of sub screen.

>To ilustrate what is a sub screen you can take as example the previous example.
>
>This screen is divided in two :
>- Main Screen:
>   -    Sub Screen 1 (Text: "Display text")
>   -   Sub Screen 2 (Text: "Display text2")
>
> The lib is purly base on this principe so every Sub Screen can have it's on sub screen etc ...

Each sub screen will have it's own management of the display of the text so with further improvement on the lib each sub screen can be entirely customize withoud affecting the other screen around

It's objectif is to have a easy and yet powerfull screen that can be share between thread

>And an other objectif is to use as little external lib as possible 
>#### Lib use now:
>- os
>

## How to use it 

First you need to create a screen

Once you have a screen you can split it in multiple sub screen

After that the Main is basicly use only to refresh the sub screen and every sub screen split are going to be "useless" for the user

>> Two diffent sub screen can be pass to two Thread\
>> Be CAREFULL one sub screen should not be pass to two different Thread this can cause unexpeted behavior

## Function

>> screen(name : str) // Main Class

Every function are from screen.
>> This function split the screen in sub screen ratio is the proportion that the first screen will take on the mother screen
>> split_horizontally(ratio : float)\
>> split_vertical(ratio : float)

>> append(message : str) // append a message to the bottom of the screen

>> clear() // clear the screen

>> rewwrite_last_line(message) // replace the last line
 
>> get_screen(indice: int) //return the subscreen indice = 0 or 1 

## Example
>>This example show how to display the screen on the termial
```python
import terminapy as tp

if __name__ == "__main__":
    screen = tp.screen()
    while True:
        screen.draw_terminal_screen()
```

>>This example show how to split the screen vertically in the middle
```python
import terminapy as tp

if __name__ == "__main__":
    screen = tp.screen()
    screen.split_vertical(0.5)
    while True:
        screen.draw_terminal_screen()

```