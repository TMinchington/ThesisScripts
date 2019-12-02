class TraceTrack:

    family_ls = []
    start_dic = {}
    end_dic = {}
    tracks_dic = {}

    def __init__(self, track_id: str, startx: float, starty: float, endx: float, endy: float, startt: float, endt: float):

        self.trackID = track_id
        self.startX = float(startx)
        self.startY = float(starty)
        self.endX = float(endx)
        self.endY = float(endy)
        self.startT = startt
        self.endT = endt
        self.parent = None
        self.children = []
        self.family = None
        self.generation = 0
        self.heritage = None

        try:

            TraceTrack.start_dic[self.startT].append(self.trackID)

        except KeyError:

            TraceTrack.start_dic[self.startT] = [self.trackID]


        TraceTrack.tracks_dic[self.trackID] = self

        try:

            TraceTrack.end_dic[self.endT].append(self.trackID)

        except KeyError:

            TraceTrack.end_dic[self.endT] = [self.trackID]

    def __str__(self):

        parent = self.parent

        if parent is not None:

            parent = parent.trackID

        return f"===================\nID: {self.trackID}\n-------------------\nparent: {parent}" \
               f"\nfamily: {self.family}" \
               f"\ngeneration: {self.generation}" \
               f"\nheritage: {self.heritage}" \
               f"\nchildren: {(self.children_string())}" \
               f"\nstart_pos: {(self.startX, self.startY)}" \
               f"\nend_pos: {(self.endX, self.endY)}" \
               f"\ntime: {self.startT} - {self.endT}" \
               f"\n===================\n"

    def children_string(self):

        if len(self.children) == 0:

            return None

        return ', '.join([x.trackID for x in self.children])

    def add_child(self, child, main_obj=True):

        self.children.append(child)
        child.parent = self
        # print(self.children)
        path = ''
        if main_obj:

            if self.family is None and child.family is None:
                path=1
                print('+++', self.family)
                new_fam = self.get_family()


                self.family = new_fam
                print('++++++', self.family)
                for child in self.children:

                    child.family = new_fam

                    child.update_fam()

                print('++++++', [x.family for x in self.children])

            elif self.family is None and child.family is not None:
                path = 2
                self.family = child.family

            else:
                path = 3
                for child in self.children:

                    child.family = self.family
                    child.update_fam()

        if child.family != self.family:

            print('error ----->', path, child.family, self.family)

        elif child.trackID == '1000000053':

            print('>>>>>>>>>>>>>>',self.trackID, child.trackID, self.family, child.family)


    def add_parent(self, parent, main_obj=True):

        print('PARENTAL ISSUES!!!!')
        exit()

        if main_obj:

            self.parent = parent

            if parent.family is None:

                parent.family = self.family

            else:

                self.update_fam()

    def get_family(self):

        if len(TraceTrack.family_ls) == 0:

            TraceTrack.family_ls.append(1)

            return 1

        current_family = TraceTrack.family_ls[-1]

        TraceTrack.family_ls.append(current_family+1)

        return current_family+1

    def update_fam(self):
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print(self.family, self.parent.family)

        self.family = self.parent.family
        # print(self.family, self.parent.family, TraceTrack.tracks_dic[self.trackID].family)
        # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        for child in self.children:
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            child.update_fam()

            print(2, child.family, self.family)


    def distance_from_end(self, other_track):

        return ((self.endX - other_track.startX)**2 + (self.endY - other_track.startY)**2)**0.5

    def distance_from_start(self, other_track):

        return ((self.startX - other_track.endX)**2 + (self.startY - other_track.endY)**2)**0.5

    def two_closest(self, start_ls):

        dis_dic = {}

        for child in start_ls:
            # print(child)
            dis_dic[self.distance_from_end(TraceTrack.tracks_dic[child])] = child


        dis_ls = sorted(list(dis_dic))
        out_ls = []

        for x in range(0, 2):

            out_ls.append(dis_dic[dis_ls[x]])

        return out_ls

    def update_child_gen(self, parent_her_code):

        self.generation = self.parent.generation + 1

        counter = 1
        self.heritage = parent_her_code
        # print(self.family, self.heritage)
        if len(self.children) != 0:

            for child in self.children:
                her_code = parent_her_code + '-' +str(counter)
                child.update_child_gen(her_code)
                counter += 1

    def info_ls(self):

        if self.parent is None:

            return [self.family, self.generation, self.heritage, 'None', self.startT, self.endT]

        else:

            return [self.family, self.generation, self.heritage, self.parent.trackID, self.startT, self.endT]

    def am_i_closest(self, child_ls, other_ls):

        from numpy import mean

        temp_dis_dic = {}

        for x in other_ls:

            dis_ls = []

            for y in child_ls:

                dis_ls.append(TraceTrack.tracks_dic[x].distance_from_end(TraceTrack.tracks_dic[y]))

            temp_dis_dic[mean(dis_ls)] = x

        return self.trackID == temp_dis_dic[min(temp_dis_dic)]

    @classmethod
    def minimise_distance(cls, grp1, grp2):

        # grp1 on should be potential parents so use end coordiantes endX etc
        # grp2 should be children so use startX etc

        import itertools

        def get_distance(co1, co2):

            x1 = co1[0]
            y1 = co1[1]
            x2 = co2[0]
            y2 = co2[1]

            dis = (x1 - x2) ** 2 + (y1 - y2) ** 2

            return dis

        def divide_ls(ls, n):

            ls = list(ls)
            out_ls = []

            for i in range(0, len(ls), n):
                out_ls.append(ls[i:i + n])

            return out_ls
        l1 = len(grp1)
        l2 = len(grp2)
        if len(grp1)*2 != len(grp2):

            # print(grp1, grp2)

            difference = len(grp1)*2 - len(grp2)
            
            blanks = ['blank']*difference

            grp2 += blanks

            # print(grp1, grp2)

            # exit(f'no match {len(grp1)*2} {len(grp1)}')

        dis_dic = {}
        print('>>>>>>>>>>>>>> itter', l1, l2)
        print(grp1)
        print(grp2)
        
        for x in itertools.permutations(grp1):

            for y in itertools.permutations(grp2):

                div_ls = divide_ls(y, 2)

                xi_dis = 0
                temp_xi_child = []

                # print('-------------------')

                for xi in range(0, len(x)):

                    xco = x[xi]

                    for yco in div_ls[xi]:
                        # print(3, l1, l2, xco, yco)

                        if yco == 'blank':

                            temp_xi_child.append((xco, yco))

                            continue

                        xobject = cls.tracks_dic[xco]
                        yobject = cls.tracks_dic[yco]

                        xcoords = (xobject.endX, xobject.endY)
                        ycoords = (yobject.startX, yobject.startY)

                        xi_dis += get_distance(xcoords, ycoords)

                        temp_xi_child.append((xco, yco))

                dis_dic[xi_dis] = temp_xi_child.copy()

        smallest = dis_dic[min(dis_dic)]

        for sm in smallest:

            if sm[1] == 'blank':

                continue

            parentobj = cls.tracks_dic[sm[0]]
            childobj = cls.tracks_dic[sm[1]]

            parentobj.add_child(childobj)

    @classmethod
    def new_fam(cls):

        if len(cls.family_ls) == 0:

            cls.family_ls.append(0)
            return 0

        else:

            new_fam = cls.family_ls[-1] + 1
            cls.family_ls.append(new_fam)
            return new_fam


    @classmethod
    def get_generations(cls):

        from pprint import pprint as pp

        for track in cls.tracks_dic:

            track_obj = cls.tracks_dic[track]

            if track_obj.parent is None:

                track_obj.generation = 0
                track_obj.heritage = str(track_obj.family)

                if len(track_obj.children) != 0:
                    counter = 1
                    for child in track_obj.children:
                        print(child.family, track_obj.family, child.family == track_obj.family)
                        child.update_child_gen(str(track_obj.family) + '-' + str(counter))

                        counter += 1


    @classmethod
    def build_families(cls):

        from pprint import pprint as pp

        for end in cls.end_dic:

            print(end, cls.end_dic[end])

        for time_point in cls.start_dic:

            for track in cls.start_dic[time_point]:

                track_obj = cls.tracks_dic[track]

                track_end = track_obj.endT

                if track_end+1 not in cls.start_dic:

                    continue

                if len(cls.end_dic[track_end]) == 1 and 0 != len(cls.start_dic[track_end+1]) <= 2:

                    try:

                        for child in cls.start_dic[track_end+1]:
                            # print('_____>', child)
                            track_obj.add_child(cls.tracks_dic[child])

                    except KeyError:

                        continue

                elif len(cls.end_dic[track_end]) != 1 and 0 != len(cls.start_dic[track_end+1]) <= 2:

                    if track_obj.am_i_closest(cls.start_dic[track_end+1], cls.end_dic[track_end]):

                        for child in track_obj.two_closest(cls.start_dic[track_end + 1]):
                            # print('_____>', child)
                            track_obj.add_child(cls.tracks_dic[child])

                    else:

                        continue

                else:

                    try:

                        for child in track_obj.two_closest(cls.start_dic[track_end + 1]):
                            # print('_____>', child)
                            track_obj.add_child(cls.tracks_dic[child])

                    except KeyError:

                        continue

        for track in cls.tracks_dic:
            # tkob == track object
            # here I am just ensuring that the track belong to the right family, if they don't then the code terminates
            tkob = cls.tracks_dic[track]

            if tkob.family is None:

                tkob.family = tkob.get_family()

            print(tkob.trackID, tkob.heritage, tkob.family, [x.family for x in tkob.children])

            for x in [x.family for x in tkob.children]:

                if x != tkob.family:
                    print('<<<<<<<<<<<<<<<<<<<<<<<<<< EXITING HERE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    print(tkob)
                    for child in tkob.children:
                        print(child)
                    print('<<<<<<<<<<<<<<<<<<<<<<<<<< EXITING HERE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

                    for track in cls.tracks_dic:

                        if cls.tracks_dic[track].parent is None:

                            print(track, cls.tracks_dic[track].family, cls.tracks_dic[track].generation,
                                  cls.tracks_dic[track].heritage, 'None',
                                  cls.tracks_dic[track].startT, cls.tracks_dic[track].endT)
                        else:

                            print(track, cls.tracks_dic[track].family, cls.tracks_dic[track].generation, cls.tracks_dic[track].heritage, cls.tracks_dic[track].parent.trackID, cls.tracks_dic[track].startT, cls.tracks_dic[track].endT)

                    exit()

        cls.get_generations()


    @classmethod
    def build_families_new(cls):

        intersect_points = {}

        gen0_ls = []
        child_starts = []
        children_ls = []

        for start_point in cls.start_dic:

            if start_point - 1 not in cls.end_dic:

                # print(start_point)

                for trackID in cls.start_dic[start_point]:

                    gen0_ls.append(trackID)

                    cls.tracks_dic[trackID].family = cls.new_fam()

            else:

                child_starts.append(start_point)

                for trackID in cls.start_dic[start_point]:

                    children_ls.append(trackID)

        for start_point in child_starts:

            starters = cls.start_dic[start_point]

            enders = cls.end_dic[start_point-1]

            print('1', len(starters), len(enders))

            single_points = [x for x in starters if x in enders]

            # print(single_points)
            # exit()
            TraceTrack.minimise_distance(enders, starters)

        cls.get_generations()

        for track in cls.tracks_dic:

            if cls.tracks_dic[track].parent is None:

                print(track, cls.tracks_dic[track].family, cls.tracks_dic[track].generation,
                      cls.tracks_dic[track].heritage, 'None',
                      cls.tracks_dic[track].startT, cls.tracks_dic[track].endT)
            else:

                print(track, cls.tracks_dic[track].family, cls.tracks_dic[track].generation,
                      cls.tracks_dic[track].heritage, cls.tracks_dic[track].parent.trackID,
                      cls.tracks_dic[track].startT, cls.tracks_dic[track].endT)


def import_tracks(track_file):

    """
    cycles through an imaris output csv file of individual tracks and creates track objects and adds them to a dictionary
    using the track ids as keys

    :param track_file:
    :return dictionary_of_tracks:
    """

    track_info_dick = {}
    head_line = False

    with open(track_file) as open_track_file:

        for line in open_track_file:

            if not head_line and not line.startswith('Variable'):

                continue

            elif line.startswith('Variable'):

                head_line = True
                print('header: ', line)
                continue

            split_line = line.strip().split(',')

            if len(split_line) != 10:

                continue

            vari, val, unit, cat, chan, collection, time, trackid, spot_id, dunno = split_line

            # print(vari, val, unit, cat, chan, collection, time, trackid, spot_id, dunno)

            if trackid == '':
                continue

            try:

                time = int(time)

            except ValueError:

                continue

            if trackid not in track_info_dick:

                track_info_dick[trackid] = {vari: {chan: {time: val}}}

                continue

            try:

                track_info_dick[trackid][vari][chan][time] = val

            except KeyError:

                try:
                    track_info_dick[trackid][vari][chan] = {time: val}

                except KeyError:

                    track_info_dick[trackid][vari] = {chan: {time: val}}

    # from pprint import pprint as pp
    #
    # pp(track_info_dick)

    return track_info_dick


def create_track_objects(track_info_dick):

    track_objects = {}

    for track in track_info_dick:
        # print(track_info_dick[track]['Position X'])
        startT = min(track_info_dick[track]['Position X'][''])
        endT = max(track_info_dick[track]['Position X'][''])

        startX = track_info_dick[track]['Position X'][''][startT]
        endX = track_info_dick[track]['Position X'][''][endT]


        startY = track_info_dick[track]['Position Y'][''][startT]
        endY = track_info_dick[track]['Position Y'][''][endT]

        track_objects[track] = TraceTrack(track, startX, startY, endX, endY, startT, endT)

        print(track_objects[track])

    print(TraceTrack.start_dic)
    print(TraceTrack.end_dic)


def output_data(data_dic, outpath, time_interval_mins):
    print('outputting')
    with open(outpath, 'w') as open_out:

        open_out.write('time\thours\tdays\ttrack\tfamily\tgeneration\tcell\tparent\tvariable\tchannel\tvalue\tnorm_interval\tnorm_zero\n')

        for track in data_dic:
            print(track)
            for variable in data_dic[track]:

                for chan in data_dic[track][variable]:

                    min_time = min(list(data_dic[track][variable][chan]))

                    for time in data_dic[track][variable][chan]:

                        value = float(data_dic[track][variable][chan][time])

                        try:

                            norm_interval = value - float(data_dic[track][variable][chan][time-1])

                        except KeyError:

                            norm_interval = 0

                        norm_zero = value - float(data_dic[track][variable][chan][min_time])
                        # print(TraceTrack.tracks_dic[track].info_ls())
                        hours = float(time)*time_interval_mins/60
                        days = hours / 24

                        out_ls = [time, hours, days, track] + TraceTrack.tracks_dic[track].info_ls()[:-2] + [variable, chan, value,
                                                                                           norm_interval, norm_zero]

                        outstr = '\t'.join([str(x) for x in out_ls])+'\n'

                        open_out.write(outstr)

def make_full_paths(data_dic, outpath2, time_interval_mins):

    terminal_tracks = []
    heritage_code_ls = []

    heritage_dic = {}

    with open(outpath2, 'w') as open_out2:

        open_out2.write(
            'time\thours\tdays\ttrack\tactual\tfamily\tgeneration\tcell\tparent\tvariable\tchannel\tvalue\tnorm_interval\tnorm_zero\n')

        for track in TraceTrack.tracks_dic:

            track_obj = TraceTrack.tracks_dic[track]
            heritage_dic[track_obj.heritage] = track_obj.trackID
            if len(track_obj.children) == 0:

                terminal_tracks.append(track)
                heritage_code_ls.append(track_obj.heritage)

        for i in range(0, len(terminal_tracks)):

            track, heritage_code = terminal_tracks[i], heritage_code_ls[i]

            print(track, heritage_code, TraceTrack.tracks_dic[track].family)

            if heritage_code == 'None':

                continue
            heritage_list = heritage_code.split('-')
            for ii in range(0, len(heritage_code)):

                act_cell = '-'.join(heritage_list[:ii+1])
                act_trackID = heritage_dic[act_cell]

                for variable in data_dic[act_trackID]:

                    for chan in data_dic[act_trackID][variable]:

                        if ii == 0:

                            min_time = min(list(data_dic[act_trackID][variable][chan]))
                            zero_val = float(data_dic[act_trackID][variable][chan][min_time])

                        for time in data_dic[act_trackID][variable][chan]:

                            value = float(data_dic[act_trackID][variable][chan][time])



                            try:

                                norm_interval = value - float(data_dic[act_trackID][variable][chan][time-1])

                            except KeyError:

                                norm_interval = 0

                            norm_zero = value - zero_val

                            # print(Traceact_trackID.act_trackIDs_dic[act_trackID].info_ls())
                            hours = float(time)*time_interval_mins/60
                            days = hours / 24

                            out_ls = [time, hours, days, track, act_cell] + TraceTrack.tracks_dic[track].info_ls()[:-2] + [variable, chan, value,
                                                                                               norm_interval, norm_zero]

                            outstr = '\t'.join([str(x) for x in out_ls])+'\n'

                            open_out2.write(outstr)



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('track_file', type=str, help="output from imaris in one file, should be output as csv details")
    parser.add_argument('--time', default=10, type=float, help="interval between frames in mins")

    args = parser.parse_args()

    if not '.csv' in args.track_file:

        exit('Error: Expected file extension CSV')

    outpath = args.track_file.replace('.csv', '-joined.csv')
    outpath2 = args.track_file.replace('.csv', '-joined_full_track.csv')

    track_info = import_tracks(args.track_file)

    create_track_objects(track_info)
    print('track_build -------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # TraceTrack.build_families()
    TraceTrack.build_families_new()

    print('start out -------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    output_data(track_info, outpath, args.time)
    #
    make_full_paths(track_info, outpath2, args.time)