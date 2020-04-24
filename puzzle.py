from relationship_enum import Relationship

counter = 0


# param listesindeki elemanların niteliklerini içermeyen
# elemanları için combination_list havuzunu süzer. param, sonuç tablosu ile benzer genişliktedir.
def get_possibility_list(param: list, combinations_list: list):
    lst = []
    for comb in combinations_list:
        checked = True
        for elm in param:
            for i in range(len(elm)):
                if elm[i] == comb[i]:
                    checked = False
                    break
            if checked is False:
                break
        if checked is True:
            lst.append(comb)
    return lst


# Logic Puzzel için temel sınıf
class Puzzle:
    variables = []  # values list
    keys = []  # variable name list
    conditions = []  # olası durumlar listesi [['Dilhan', 'Naz', 'Ayakkabı', 6], ['İsmail', 'Trabzon', 'Cam Eşya', 5],....
    solution = None

    def __init__(self):
        """

        :rtype: object
        """
        self.condition_ext_rules = []  # Uzatılmış kısıt listesi
        self.condition_rules = []  # Temel kısıt listesi

    # Puzzle için bir değişkenin değer kümesini girmek için kullanılır
    # add_values("İsim", ["Dilhan", "İsmail", "Leman", "Rana", "Selim"])
    def add_values(self, key_name, key_values):
        self.keys.append(key_name)
        self.variables.append(key_values)
        self.__add_all_condition(key_values)

    # Olası durumlar kümesi için tüm kombinasyonları üretir,
    # __add_all_condition(["Dilhan", "İsmail", "Leman", "Rana", "Selim"])
    # __add_all_condition(["Kilit", "Cenk", "Gümüşçü", "Trabzon", "Naz"])
    def __add_all_condition(self, key_values):
        if not self.conditions:
            self.conditions = key_values
        else:
            lst = []
            for elm in self.conditions:
                for val in key_values:
                    if isinstance(elm, list):
                        lst.append(elm + [val])
                    else:
                        lst.append([elm, val])
            self.conditions = lst

    # Puzzle için bir kural ekler.
    # add_condition(Relationship.EQ, {"Koleksiyon": "Cam Eşya"}, {"Soyisim": "Gümüşçü"}, "Süre", 2)
    # Cam Eşya koleksiyonu yapan kişinin koleksiyon süresi, Gümüşçü soyisimli kişiden koleksiyon süresinin iki fazlası kadar.
    # EQ : Koşul ifadesi, Relationship enum tipinde veri
    # val1: {key_name: key_value}
    # val2: {key_name: key_value}
    # key: key_name - ortak anahtar ismi
    # added_value: eklenti değeri
    def add_condition(self, EQ, val1: dict, val2: dict, key=None, added_value=None):
        if key is None:
            self.condition_rules.append([EQ, val1, val2, None, None])
        else:
            self.condition_ext_rules.append([EQ, val1, val2, key, added_value])
            self.condition_rules.append([Relationship.NE, val1, val2, None, None])

    # mevcut bir değer ataması için, koşulları sorgular.
    # elm : ['Leman', 'Cenk', 'Metal Para', 7]
    # tüm koşullara uygunsa True değeri döner
    # koşul test edilemiyorsa pass değeri döner
    def __condition_filter(self, condition, elm):
        key_name1 = list(condition[1].keys())[0]
        key_value1 = condition[1][key_name1]
        key_index1 = self.keys.index(key_name1)

        key_name2 = list(condition[2].keys())[0]
        key_value2 = condition[2][key_name2]
        key_index2 = self.keys.index(key_name2)

        if key_value1 == elm[key_index1]:
            if condition[0] == Relationship.EQ:
                if key_value2 == elm[key_index2]:
                    return True
            if condition[0] == Relationship.NE:
                if key_value2 != elm[key_index2]:
                    return True
            if condition[0] == Relationship.GT:
                if key_value2 > elm[key_index2]:
                    return True
            if condition[0] == Relationship.LT:
                if key_value2 < elm[key_index2]:
                    return True
            if condition[0] == Relationship.LE:
                if key_value2 <= elm[key_index2]:
                    return True
            if condition[0] == Relationship.GE:
                if key_value2 >= elm[key_index2]:
                    return True
            return False
        else:
            if condition[0] == Relationship.EQ:
                if key_value2 == elm[key_index2]:
                    return False
            return "Pass"

    # Tüm çözüm ağacını temel kurallara göre temizler.
    # Çözümün bir parçası olamayak elemanlar silinir.
    # Örn: Dilhan Halı Koleksiyonu yapmaz. Koşulu var ise
    # Çözüm ağacından Dilhan ve Halı içeren çözümleri siler
    def __clean_condition(self):
        lst = []
        for elm in self.conditions:
            exit_code = True
            for cond in self.condition_rules:
                if not self.__condition_filter(cond, elm):
                    exit_code = False
                    break
            if exit_code:
                lst.append(elm)

        self.conditions = lst

    # Tam bir olası çözüm kümesi oluştuğunda yapılabicek kural testlerini yapar.
    def __check_ext_condition(self, initial_table):
        res = True
        for con in self.condition_ext_rules:
            ref = con[3]
            ref_index = self.keys.index(ref)
            ref_val = con[4]

            key_name1 = list(con[1].keys())[0]
            key_value1 = con[1][key_name1]
            key_index1 = self.keys.index(key_name1)

            key_name2 = list(con[2].keys())[0]
            key_value2 = con[2][key_name2]
            key_index2 = self.keys.index(key_name2)

            for elm in initial_table:
                if elm[key_index1] == key_value1:
                    c1 = elm[ref_index]
                if elm[key_index2] == key_value2:
                    c2 = elm[ref_index]
            if ref_val is None:
                ref_val = 0

            if con[0] == Relationship.EQ:
                if c1 - ref_val == c2:
                    res = True
                    continue
            if con[0] == Relationship.NE:
                if c1 - ref_val != c2:
                    res = True
                    continue
            if con[0] == Relationship.GE:
                if c1 - ref_val >= c2:
                    res = True
                    continue
            if con[0] == Relationship.LE:
                if c1 - ref_val <= c2:
                    res = True
                    continue
            if con[0] == Relationship.LT:
                if c1 - ref_val < c2:
                    res = True
                    continue
            if con[0] == Relationship.GT:
                if c1 - ref_val > c2:
                    res = True
                    continue
            res = False
            break
        if res:
            return True
        else:
            return False

    # Çözüm kümesini referans değişkenin değerleri için ayırır.
    def __slice_conditions(self, var_names, conditions):
        lst = [[] for i in var_names]
        for cd in conditions:
            lst[var_names.index(cd[0])].append(cd)
        return lst

    # Çözüm için temel metod
    def solve(self):
        self.__clean_condition()  # Öncelikli temizleme iterasyon sayısını yüksek oranda düşürür.
        int_table = [[] for i in self.variables[0]]  # Boş bir çözüm kümesi oluştur.
        data = self.__slice_conditions(self.variables[0],
                                       self.conditions)  # Temel değişken için tüm çözüm ağacını gruplandır.
        data.sort(key=len)  # En kısıtlı değişkenden artan sıralama
        if self.__backtracking_solver(int_table, data):
            print("Sonuç Bulundu!")
            return True
        else:
            print("Sonuç Bulunamadı!")
            return False

    # recursive backtracking method
    def __backtracking_solver(self, init_table, csp):
        global counter
        counter += 1  # iterasyon sayacı
        print("iteration: ", counter)
        row = -1
        if len(init_table[len(self.variables[0]) - 1]) != 0:  # Olası çözüm tablosu dolu mu?
            if self.__check_ext_condition(init_table):  # Tabloyu denetle
                self.solution = init_table
                return True
            else:
                return False
        else:
            for i in range(len(self.variables[0])):  # Olası çözüm tablosunda ilk boş satırı bul?
                if len(init_table[i]) == 0:
                    row = i
                    break
            ps_list = get_possibility_list(init_table, csp[row])  # Satır için olası çözüm kümesini getir
            if len(ps_list) != 0:  # Liste boş mu?
                for elm in ps_list:
                    if elm:
                        init_table[row] = elm
                        if -1 < row < len(self.variables[0]):
                            init_table[row + 1:] = [[] for i in init_table[row + 1:]]
                        if self.__backtracking_solver(init_table, csp):
                            return True
            else:
                init_table[row - 1:] = [[] for i in init_table[row - 1:]]
                return False
