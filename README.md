# DELU_V3
DELU Version 3.0

How To Use DELU V3 Package

## 1. Importing Package

    import DELU


## 2. Initialize Bot

    system = DELU.system(["room_name1", "room_name2", ...])
    controller = DELU.controller()


## 3. FME Message edit
    FME.edit( Message ) -> bool
        * Automatically edit all FME contents.
        * FME Grammar: ///FME:TYPE:ARGUMENTS///
        * FME Types: Meal, Time, Date, Dday, News
