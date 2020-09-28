# Actions

MainMenu.start():
    assert MainMenu.model
    try:
        MainMenu.model.loop()

Model.loop():
    Model.scheduler.invoke_next()

EventQueue.invoke_next():
    event = EventQueue.heap[0]
    event.func(EventQueue, event)

Actor.event = Actor.scheduler.schedule(0, Actor.act)

Actor.act():
    try:
        action = Actor.ai.plan()
    ...
    assert action is action.plan()
    action.act()

PlayerControl(AI).act():
    event = PlayerControl.actor.event
          = Actor.scheduler.schedule(0, Actor.act)
          = EventQueue.schedule(0, Actor.act)

            EventQueue.schedule() -> Event:
                event = Event(tick+interval, id, func)
                event = Event(..., Actor.act)
                heapq.heappush(EventQueue.heap, event)
                heapq.heappush(EventQueue.heap, Actor.act)

            EventQueue.invoke_next():
                event.func(EventQueue, event)
                = event.func(EventQueue, Actor.act)
 
    while event is PlayerControl.actor.event:
        PlayerControl.next_action = PlayerReady(...model).loop()
        ...
        PlayerControl.next_action.plan().act()
        = PlayerReady(...model).loop().plan().act()

        = Action.act()

PlayerReady(AreaState["Action"])
PlayerReady(AreaState(Generic[T], State(Generic[T], tcod.event.EventDispatch[T])))
PlayerReady(AreaState(State(tcod.event.EventDispatch["Action"])))



PlayerReady(AreaState["Action"]):
    cmd_{symbol}() -> Action:
        return ... common.[Action](*args)



