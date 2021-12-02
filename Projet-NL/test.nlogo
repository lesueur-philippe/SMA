breed [boxes box]
breed [humans human]

patches-own [
    isDestination?
]

humans-own [
    capacity
    vision
    carrying
]

boxes-own [
    weight
]

to setup
    clear-all
    setup-patches
    setup-boxes
    setup-humans
    reset-ticks
    ask turtles [
        set label-color black
    ]
end

to go
    ask humans [
        ifelse carrying > 0 [
            go-to-drop
        ] [
            find-box
        ]
    ]
    pickup-box
    drop-boxes
    tick
end

to go-to-drop
    set heading towards one-of patches with [isDestination?]
    fd 1
end

to setup-patches
    ask patches [
        set pcolor white
        set isDestination? false
    ]

    ask one-of patches [
        set pcolor pink
        set isDestination? true
    ]
end

to setup-boxes
    create-boxes nbBoxes [
        set shape "box"
        set color brown
        setxy random-xcor random-ycor
        set weight (random 8 + 2)
        set label weight
    ]
end

to setup-humans
    create-humans nbHumans [
        set shape "person"
        set color black
        setxy random-xcor random-ycor
        set capacity 10
        set vision 3
    ]
end

to find-box

    set heading towards (last (sort-on [count-boxes] patches in-radius vision))
    fd 1
    ;; rt 90 * (random 3 - 1)
    ;; fd 1
end

to pickup-box
    ask humans [
        if (count-boxes >= 1) [ 
            let b one-of boxes-here 
            if get-weight b + carrying < capacity [
                carry self b
            ]
        ]
    ]
end

to carry [hmn bx]
    ask hmn [
        set carrying carrying + (get-weight bx)
        set color brown
    ]
    ask bx [
        die
    ]
end

to drop-boxes
    ask humans [
        if [isDestination?] of patch-here = true [
            set color black
            set carrying 0
        ]
    ]
end

to-report count-boxes
    report count boxes-here
end

to-report get-weight [bx]
    report [weight] of bx
end