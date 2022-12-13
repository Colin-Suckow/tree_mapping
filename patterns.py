import math

def vertical_rg(points, t):
    def pattern(i):
        if points[i] is not None:
            r = int((math.cos(t - points[i][1] * math.pi) / 2 + 0.5) * 64)
            g = int((math.cos(t - points[i][1] * math.pi + (math.pi / 2)) / 2 + 0.5) * 32)
            return (g, r, 0)
        else:
            return (0, 0, 0)
    return pattern

def vertical_rg_sharp(points, t):
    def pattern(i):
        if points[i] is not None:
            x = max(0, min((t - points[i][1]) % 1, 1))
            r = int(((1 - (1 - x * 4)) ** 32) * 64)
            g = int(((1 - (1 - (x - 0.5) * 4)) ** 32) * 32)
            
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            return (g, r, 0)
        else:
            return (0, 0, 0)
    return pattern


def vertical_rg_half(points, t):
    def pattern(i):
        if points[i] is not None:
            x = max(0, min((t - points[i][0]) % 1, 1))
            
            if x > 0.5:
                return (64, 0, 0)
            else:
                return (0, 128, 0)
        else:
            return (0, 0, 32)
    return pattern

def vertical_rg_rot(points, t):
    slice = 1
    def pattern(i):
        r = 0
        g = 0
        b = 0
        if points[i] is not None:
            p = points[i]
            r = math.sqrt((p[0] - 0.5) ** 2 + (p[2] - 0.5) ** 2)
            try:
                theta = math.atan2((p[0] - 0.5), (p[2] - 0.5))
            except:
                theta = 0
            theta += math.pi
            #theta = theta / (math.pi * 2)
            mt = ((-t * 6) + (p[1] * 8)) % (math.pi * 2)
            if abs(theta - mt) < slice or abs(theta - mt) > math.pi * 2 - slice:
                g = 1
            else:
                r = 1
            return (int(g * 64), int(r * 64), 0)
        else:
            return (0, 0, 0)
    return pattern

def rot_disc(points, t):
    def pattern(i):
        if points[i] is not None:
            r = 0
            g = 0
            b = 0
            p = points[i]
            ra = math.sqrt((p[0] - 0.5) ** 2 + (p[2] - 0.5) ** 2)
            try:
                theta = math.atan2((p[0] - 0.5), (p[2] - 0.5))
            except:
                theta = 0
            theta += math.pi
            theta = theta / (math.pi * 2)
            
            if p[1] <= 0.333:
                mt = t % 1
                if abs(theta - mt) < 0.1:
                    g = 1
            elif p[1] <= 0.666:
                mt = (t + 0.33) % 1
                if abs(theta - mt) < 0.1:
                    r = 1
            else:
                mt = (t + 0.66) % 1
                if abs(theta - mt) < 0.1:
                    b = 1


            if abs(theta - mt) < 0.1:
                g = 1
            else:
                g = 0
            return (int(g * 64), int(r * 64), int(b * 64))
        else:
            return (0, 0, 0)
    return pattern

def t_wave(points, t):
    def pattern(i):
        if points[i] is not None:
            g = 0
            mt = t % 1
            if abs(points[i][1] -(math.cos(mt * math.pi * 2) / 2 + 0.5)) < 0.01:
                r = 1
            else:
                r = 0

            # if abs(points[i][0] -(math.cos(mt * math.pi * 2) / 2 + 0.5)) < 0.01:
            #     g = 1
            # else:
            #     g = 0

            if abs(points[i][2] -(math.cos(mt * math.pi * 2) / 2 + 0.5)) < 0.01:
                b = 1
            else:
                b = 0
            return (g * 128, r * 128, b * 128)
        else:
            return (0, 0, 0)
    return pattern