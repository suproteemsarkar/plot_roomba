# Plot a series of x-y points

# Version 1:
# At each point, point and turn.

import math
import create2_cli
import urllib
import time
import sys

SCALING_FACTOR = 20
TIME_ROT_DELAY = 0.01

MAGIC_URL = 'https://www.wolframcloud.com/objects/user-0bd94b55-72c1-466a-8c79-c0ad96a59807/coords'
TEST_DATA = "{{{0, 0}, {1, 1}, {2, 8}, {3, 27}, {4, 64}, {5, 125}, {6, 216}, {7, 343}, {8, 512}, {9, 729}, {10, 1000}, {11, 1331}, {12, 1728}, {13, 2197}, {14, 2744}, {15, 3375}, {16, 4096}, {17, 4913}, {18, 5832}, {19, 6859}, {20, 8000}, {21, 9261}, {22, 10648}, {23, 12167}, {24, 13824}, {25, 15625}, {26, 17576}, {27, 19683}, {28, 21952}, {29, 24389}, {30, 27000}, {31, 29791}, {32, 32768}, {33, 35937}, {34, 39304}, {35, 42875}, {36, 46656}, {37, 50653}, {38, 54872}, {39, 59319}, {40, 64000}, {41, 68921}, {42, 74088}, {43, 79507}, {44, 85184}, {45, 91125}, {46, 97336}, {47, 103823}, {48, 110592}, {49, 117649}, {50, 125000}, {51, 132651}, {52, 140608}, {53, 148877}, {54, 157464}, {55, 166375}, {56, 175616}, {57, 185193}, {58, 195112}, {59, 205379}, {60, 216000}, {61, 226981}, {62, 238328}, {63, 250047}, {64, 262144}, {65, 274625}, {66, 287496}, {67, 300763}, {68, 314432}, {69, 328509}, {70, 343000}, {71, 357911}, {72, 373248}, {73, 389017}, {74, 405224}, {75, 421875}, {76, 438976}, {77, 456533}, {78, 474552}, {79, 493039}, {80, 512000}, {81, 531441}, {82, 551368}, {83, 571787}, {84, 592704}, {85, 614125}, {86, 636056}, {87, 658503}, {88, 681472}, {89, 704969}, {90, 729000}, {91, 753571}, {92, 778688}, {93, 804357}, {94, 830584}, {95, 857375}, {96, 884736}, {97, 912673}, {98, 941192}, {99, 970299}, {100, 1000000}, {101, 1030301}, {102, 1061208}, {103, 1092727}, {104, 1124864}, {105, 1157625}, {106, 1191016}, {107, 1225043}, {108, 1259712}, {109, 1295029}, {110, 1331000}, {111, 1367631}, {112, 1404928}, {113, 1442897}, {114, 1481544}, {115, 1520875}, {116, 1560896}, {117, 1601613}, {118, 1643032}, {119, 1685159}, {120, 1728000}, {121, 1771561}, {122, 1815848}, {123, 1860867}, {124, 1906624}, {125, 1953125}, {126, 2000376}, {127, 2048383}, {128, 2097152}, {129, 2146689}, {130, 2197000}, {131, 2248091}, {132, 2299968}, {133, 2352637}, {134, 2406104}, {135, 2460375}, {136, 2515456}, {137, 2571353}, {138, 2628072}, {139, 2685619}, {140, 2744000}, {141, 2803221}, {142, 2863288}, {143, 2924207}, {144, 2985984}, {145, 3048625}, {146, 3112136}, {147, 3176523}, {148, 3241792}, {149, 3307949}, {150, 3375000}, {151, 3442951}, {152, 3511808}, {153, 3581577}, {154, 3652264}, {155, 3723875}, {156, 3796416}, {157, 3869893}, {158, 3944312}, {159, 4019679}, {160, 4096000}, {161, 4173281}, {162, 4251528}, {163, 4330747}, {164, 4410944}, {165, 4492125}, {166, 4574296}, {167, 4657463}, {168, 4741632}, {169, 4826809}, {170, 4913000}, {171, 5000211}, {172, 5088448}, {173, 5177717}, {174, 5268024}, {175, 5359375}, {176, 5451776}, {177, 5545233}, {178, 5639752}, {179, 5735339}, {180, 5832000}, {181, 5929741}, {182, 6028568}, {183, 6128487}, {184, 6229504}, {185, 6331625}, {186, 6434856}, {187, 6539203}, {188, 6644672}, {189, 6751269}, {190, 6859000}, {191, 6967871}, {192, 7077888}, {193, 7189057}, {194, 7301384}, {195, 7414875}, {196, 7529536}, {197, 7645373}, {198, 7762392}, {199, 7880599}, {200, 8000000}}, {2017, 9, 16, 17, 57, 19.234923`8.036665436084373}}[<||>]"
HACKMIT_POINTS = [[0, 4], [0, 2], [1, 2], [1,4], [1,0], [2,0], [2,4], [3,4], [3,2], [2,2], [3,2], [3,0], [4,0], [4,4], [4.5, 0], [5, 4], [5, 0], [6.5, 0], [6.5, 4], [6.5, 0], [8.5, 0], [8.5, 4], [8, 4], [9, 4], [8.5, 4], [8.5, 0]]
app = None

class RoombaNavigate():
    position = (0,0)    #in units of scaling
    theta = 0           #radians from x-axis
    prev_data = ''
    seconds_per_degree = 0.024  #found experimentally
    seconds_per_dist_unit = 0.2   #tuned for best experience
    def __init__(self):
        print 'start'

    def start(self):
        if len(sys.argv) > 1:
            print sys.argv
            if sys.argv[1] == '-hackmit':
                print 'HACKMIT'
                self.plot_xy(HACKMIT_POINTS)
            else:
                print 'Unknown commands'
        while True:
            print('loop start')
            try:
                file_handler = urllib.urlopen(MAGIC_URL)
                data = file_handler.readline()
            except IOError:
                print 'Connection Error: could not connect'
                data = TEST_DATA
                continue
            if len(sys.argv) > 1 and sys.argv[1] == "-l":
                data = "{{{0., 0.}, {0.25, 6.279051952931337}, {0.5, 12.533323356430426}, {0.75, 18.73813145857246}, {1., 24.86898871648548}, {1.25, 30.901699437494738}, {1.5, 36.812455268467794}, {1.75, 42.577929156507274}, {2., 48.17536741017153}, {2.25, 53.58267949789967}, {2.5, 58.778525229247315}, {2.75, 63.74239897486896}, {3., 68.45471059286886}, {3.25, 72.89686274214115}, {3.5, 77.05132427757893}, {3.75, 80.90169943749474}, {4., 84.43279255020151}, {4.25, 87.63066800438637}, {4.5, 90.48270524660195}, {4.75, 92.97764858882513}, {5., 95.10565162951535}, {5.25, 96.85831611286311}, {5.5, 98.22872507286885}, {5.75, 99.21147013144778}, {6., 99.80267284282715}, {6.25, 100.}, {6.5, 99.80267284282715}, {6.75, 99.21147013144778}, {7., 98.22872507286885}, {7.25, 96.85831611286312}, {7.5, 95.10565162951536}, {7.75, 92.97764858882513}, {8., 90.48270524660195}, {8.25, 87.63066800438635}, {8.5, 84.4327925502015}, {8.75, 80.90169943749474}, {9., 77.05132427757893}, {9.25, 72.89686274214114}, {9.5, 68.45471059286888}, {9.75, 63.74239897486898}, {10., 58.77852522924732}, {10.25, 53.58267949789967}, {10.5, 48.17536741017156}, {10.75, 42.57792915650729}, {11., 36.812455268467815}, {11.25, 30.901699437494752}, {11.5, 24.868988716485482}, {11.75, 18.738131458572457}, {12., 12.533323356430454}, {12.25, 6.279051952931358}, {12.5, 1.2246467991473532*^-14}, {12.75, -6.279051952931335}, {13., -12.53332335643043}, {13.25, -18.738131458572475}, {13.5, -24.8689887164855}, {13.75, -30.901699437494774}, {14., -36.81245526846783}, {14.25, -42.57792915650727}, {14.5, -48.175367410171496}, {14.75, -53.58267949789964}, {15., -58.7785252292473}, {15.25, -63.74239897486896}, {15.5, -68.45471059286888}, {15.75, -72.89686274214114}, {16., -77.05132427757894}, {16.25, -80.90169943749473}, {16.5, -84.43279255020153}, {16.75, -87.63066800438637}, {17., -90.48270524660198}, {17.25, -92.97764858882515}, {17.5, -95.10565162951535}, {17.75, -96.8583161128631}, {18., -98.22872507286887}, {18.25, -99.21147013144778}, {18.5, -99.80267284282715}, {18.75, -100.}, {19., -99.80267284282715}, {19.25, -99.21147013144778}, {19.5, -98.22872507286887}, {19.75, -96.85831611286311}, {20., -95.10565162951536}, {20.25, -92.97764858882512}, {20.5, -90.48270524660195}, {20.75, -87.63066800438634}, {21., -84.43279255020155}, {21.25, -80.90169943749476}, {21.5, -77.05132427757896}, {21.75, -72.89686274214115}, {22., -68.45471059286889}, {22.25, -63.74239897486896}, {22.5, -58.778525229247336}, {22.75, -53.58267949789963}, {23., -48.17536741017153}, {23.25, -42.577929156507224}, {23.5, -36.81245526846779}, {23.75, -30.901699437494763}, {24., -24.868988716485536}, {24.25, -18.738131458572468}, {24.5, -12.533323356430465}, {24.75, -6.279051952931327}, {25., -2.4492935982947064*^-14}, {25.25, 6.279051952931278}, {25.5, 12.533323356430417}, {25.75, 18.738131458572422}, {26., 24.86898871648549}, {26.25, 30.901699437494717}, {26.5, 36.81245526846782}, {26.75, 42.57792915650725}, {27., 48.17536741017157}, {27.25, 53.58267949789967}, {27.5, 58.77852522924736}, {27.75, 63.74239897486898}, {28., 68.45471059286893}, {28.25, 72.89686274214118}, {28.5, 77.05132427757893}, {28.75, 80.90169943749478}, {29., 84.43279255020147}, {29.25, 87.63066800438631}, {29.5, 90.48270524660194}, {29.75, 92.97764858882512}, {30., 95.10565162951535}, {30.25, 96.8583161128631}, {30.5, 98.22872507286885}, {30.75, 99.21147013144778}, {31., 99.80267284282715}, {31.25, 100.}, {31.5, 99.80267284282715}, {31.75, 99.21147013144778}, {32., 98.22872507286885}, {32.25, 96.85831611286311}, {32.5, 95.10565162951536}, {32.75, 92.97764858882516}, {33., 90.48270524660192}, {33.25, 87.63066800438634}, {33.5, 84.43279255020151}, {33.75, 80.90169943749477}, {34., 77.05132427757886}, {34.25, 72.8968627421411}, {34.5, 68.45471059286884}, {34.75, 63.742398974868976}, {35., 58.778525229247336}, {35.25, 53.58267949789972}, {35.5, 48.175367410171624}, {35.75, 42.577929156507395}, {36., 36.8124552684678}, {36.25, 30.901699437494777}, {36.5, 24.86898871648555}, {36.75, 18.738131458572568}, {37., 12.53332335643039}, {37.25, 6.279051952931339}, {37.5, 3.6739403974420595*^-14}, {37.75, -6.279051952931265}, {38., -12.533323356430317}, {38.25, -18.738131458572497}, {38.5, -24.868988716485475}, {38.75, -30.901699437494706}, {39., -36.81245526846772}, {39.25, -42.577929156507324}, {39.5, -48.17536741017155}, {39.75, -53.582679497899655}, {40., -58.77852522924728}, {40.25, -63.742398974869054}, {40.5, -68.45471059286892}, {40.75, -72.89686274214118}, {41., -77.05132427757893}, {41.25, -80.90169943749473}, {41.5, -84.43279255020157}, {41.75, -87.63066800438631}, {42., -90.4827052466019}, {42.25, -92.97764858882513}, {42.5, -95.10565162951534}, {42.75, -96.8583161128631}, {43., -98.22872507286885}, {43.25, -99.21147013144778}, {43.5, -99.80267284282715}, {43.75, -100.}, {44., -99.80267284282715}, {44.25, -99.2114701314478}, {44.5, -98.22872507286885}, {44.75, -96.85831611286312}, {45., -95.10565162951538}, {45.25, -92.97764858882516}, {45.5, -90.48270524660192}, {45.75, -87.63066800438635}, {46., -84.43279255020151}, {46.25, -80.90169943749477}, {46.5, -77.05132427757886}, {46.75, -72.89686274214111}, {47., -68.45471059286885}, {47.25, -63.742398974868976}, {47.5, -58.77852522924735}, {47.75, -53.582679497899576}, {48., -48.17536741017163}, {48.25, -42.5779291565074}, {48.5, -36.81245526846781}, {48.75, -30.90169943749479}, {49., -24.86898871648556}, {49.25, -18.73813145857258}, {49.5, -12.533323356430401}, {49.75, -6.2790519529313515}, {50., -4.898587196589413*^-14}}, {2017, 9, 16, 20, 57, 22.505329`8.104860349327026}}[<||>]"
            if data != self.prev_data:
                print('plot start')
                self.prev_data = data
                points = self.process_data(data)
                self.plot_xy(points)
                self.move_to_origin()
                print('plot stop')
            time.sleep(2)


    def process_data(self, data):
        print data
        wolfram_string = data[:-6]
        end_str = wolfram_string.rfind('}}', -2)
        points_string = wolfram_string[3:end_str + 1]
        points_array = points_string.split('}, {')
        request_time = points_array.pop()
        points_array[-1] = points_array[-1][:-1]    #Chop off the last brace
        print points_array
        points = []
        maxy = float('-inf')
        for point in points_array[:49]:             #There may be jank code here to avoid bad values
            next_point = map(float, point.split(', '))
            points.append(next_point)
            if (next_point[1] > maxy):
                maxy = next_point[1]
        for i in range(len(points)):
            points[i][1] *= SCALING_FACTOR / float(maxy)
        print points
        return points

    def move_to_origin(self):
        print 'idk'

    def plot_xy(self, points):
        self.move_to_origin()
        lastx, lasty = 0, 0
        for x, y in points:
            self.move(lastx, lasty, x, y)
            lastx, lasty = x, y

    def move(self, lastx, lasty, x, y):
        new_theta = math.atan2(y, x)
        print new_theta
        diff_theta = new_theta - self.theta
        dist = math.sqrt((x - lastx) ** 2 + (y - lasty) ** 2)
        self.theta = new_theta
        self.rotate(diff_theta)
        self.travel(dist)

    def rotate(self, angle):
        global app

        degrees = math.degrees(angle)
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360

        print 'rotate ' + str(degrees) + ' degrees'
        if degrees > 0:
            print 'time: ' + str(degrees * self.seconds_per_degree)
            app.sendCommandASCII('137 0 80 0 1')
            time.sleep(degrees * self.seconds_per_degree + TIME_ROT_DELAY)
            app.stop()
        else:
            print 'time: ' + str(-degrees * self.seconds_per_degree)
            app.sendCommandASCII('137 0 80 255 255')
            time.sleep(-degrees * self.seconds_per_degree + TIME_ROT_DELAY)
            app.stop()

    def travel(self, dist):
        global app

        app.sendCommandASCII('145 0 100 0 100')
        time.sleep(dist * self.seconds_per_dist_unit)
        app.stop()

if __name__ == "__main__":
    roomba = RoombaNavigate()
    app = create2_cli.TetheredDriveApp()
    app.sendCommandASCII('131')
    roomba.start()
