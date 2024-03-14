## YAML

Yaml is a human readable data serialization format. Used for configuration and data exchange b/w systems.

Usage

```yaml
   key: value
   nested-key:
       - item 1
       - item 2
```

It uses number of spacees for indentation.
Conventionally Two spaces are used for indentation.

Comments:
Represented by "#" character to provide description. these are ignored by yaml

# Comment

key: value # values ore listed

Scalars:
Scalars represent simple values Like strings, numbers, etc..
For ex,
String : hello
number : 43
boolean: true
null : null
Scalars don't have any indentation.

Multi-line Scalars :
This is a bit but Similar to scalars but not that much
Multi-line : |
    This is a about
    yaml file format

If Scalar value spans multiple lines  we use | and > Characters ,  otherwise it will give error.
It is also called as key for accessing inside the scalar.

Example.yaml :

  name: Samdan
  location: Vijayawada
  Profesion :student
  Hobbies :
     Playing
     Social media
     Programming
  Favourites:
     fruits :grapes
     celeb: Prabhas
  whatisthisabout:
     this is a basic outline of yaml
     File format

Finally,
If your yaml file is Syntactically correct (or) not. you can check it in "Yamlint" website.
