# Word Of The Day

<img src="https://play-lh.googleusercontent.com/BYoyK1fiFfpH8JTutWAlG_Tqo-Ati-7tLcdYijU-8_L7SQxpuYBo7tzxrzDGXk8JC4hv" width="250" height="250"/>

Word of the Day is a discord.py bot that I originally wrote for fun. 
I wanted to learn the advanced side of py with classes and states, while also working with the discord library, to create something I would actually use.
Along the way, I decided it would be good to share it.

## Interesting stuff?

-[How It Works](#how-it-works)
-[How To Launch](#)
-[TODO](#)

## How It Works

This is how the bot works.


### Drawing

> You can find detailed documentation about drawing [here][drawing-docs].

The most basic operation *Zircon* supports is `draw`ing. You can draw individual `Tile`s or `TileGraphics` objects on your `TileGrid`. a `TileGraphics` object is composed of `Tile`s. This is a powerful tool and you can implement more complex features using simple `draw` operations. In fact the component system is implemented on top of drawing, layering and input handling features.

If you use REXPaint to design your programs, the good news is that you can import your `.xp` files as well. Read more about it [here](https://hexworks.org/zircon/docs/2018-11-22-resource-handling#rexpaint-files).

You can also use `Modifier`s in your `Tile`s such as `blink`, `verticalFlip` or `glow`. For a full list, check [this](https://github.com/Hexworks/zircon/blob/master/zircon.core/src/commonMain/kotlin/org/hexworks/zircon/api/Modifiers.kt) factory object. `Modifier`s can either change the
texture (like the ones above) or the `Tile` itself:

![Modifiers](images/gifs/modifiers.gif)

### Input handling

> Read about input handling in the docs [here][input-docs].

Both the `TileGrid` and the `Screen` interfaces implement `UIEventSource` which means that you can listen for user inputs using them. This includes *key strokes* and *mouse input* as well. 

### Layering

> Layering is detailed [here][layer-docs]. For a primer on `Screen`s go [here][screen-docs].

Both the `TileGrid` and the `Screen` interfaces implement `Layerable` which means that you can add `Layer`s on top of them. Every `Layerable` can have an arbitrary amount of `Layer`s. `Layer`s are like `TileGraphics` objects and you can also have transparency in them which can be used to create fancy effects. `Component`s are also `Layer`s themselves. Take a look:

![Layers](images/layers.png)

### Text GUI Components

> You can read more about the Component System on the [documentation page][component-docs]. Color themes are detailed [here][color-theme-docs].

`Component`s are GUI controls which can be used for showing content to the user (`Label`s, `Paragraph`s, etc), enabling them to interact with your program (`Button`s, `Slider`s, etc) or to hold other components (`Panel`s for example).

These components are rather simple and you can expect them to work in a way you might be familiar with:

- You can click on them (press and release are different events).
- You can attach event listeners on them.
- Zircon implements focus handling so you can navigate between the components using the `[Tab]` key
 (forwards) or the `[Shift]+[Tab]` key stroke (backwards).
- Components can be hovered and you can also apply color themes to them.

What's more is that you can apply `ColorTheme`s to `Component`s. There are a bunch of built-in themes, and you can also create your own.

To see a full list of available `Component`s take a look at the [Components](https://github.com/Hexworks/zircon/blob/master/zircon.core/src/commonMain/kotlin/org/hexworks/zircon/api/Components.kt) factory object or navigate to the [component docs page][component-docs].

This is an example of how components look in action:

![All Components](images/gifs/all_components.gif)

### Animations:
