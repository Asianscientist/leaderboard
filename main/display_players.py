

def players(model, r):
    games=model.objects.all()
    leaders={}
    for x in games:
        data=r.zrevrange(x.name, 0, -1, withscores=True)
        for x in data:
                name, score = x[0].decode(), x[1]
                if name in leaders:
                    score=max(leaders[name], score)
                leaders[name]=score
    return leaders