def get_tables(table_list):
    returned_tables = []
    for table in table_list:
        if table == 'T1':
            returned_tables.append(table1)
        elif table == 'T2':
            returned_tables.append(table2)
        else:
            returned_tables.append(table3)
    return returned_tables
def display_table(table):
    print
    for col in table[0]:
        print "       ", col,
    print
    for col in table[0]:
        print "----------",
    table.pop(0)
    print

    for row in table:
        # print row_format.format("", *row)
        for col in row:
            print '{:{align}{width}}'.format(col, align='>', width="10"),
        print
def project_operation(table, attribute_list):
    new_table = []
    col_list = []
    if attribute_list[0] == "*":
        return table
    for attribute in attribute_list:
        if attribute != 'KC':
            col_list.append(table[0].index(attribute))
        if attribute == 'C1' or attribute == 'B1' or attribute == 'A1':
            col_list.append(table[0].index(attribute) + 1)

    if table[0].index('TC') not in col_list:
        col_list.append(table[0].index('TC'))
    col_list.sort()
    #print col_list
    temp_list = []
    for row in table:
        for col in col_list:
            temp_list.append(row[col])
        new_table.append(temp_list)
        temp_list = []
    return new_table
def make_table(table, index, value):
    new_table = [table[0]]
    for row in table[1:]:
        if int(row[index]) == int(value):
            new_table.append(row)
    return new_table
def select_operation(table, regular_conditions, security_level):
    for cond in regular_conditions:
        temp = cond.split("=")
        if temp[0] == "TC" and int(temp[1]) > int(security_level):
            print "Error: Security Level Violation"
            exit()
        index = table[0].index(temp[0])
        table = make_table(table, index, temp[1])
    #print "SELECT OPERATION"
    #display_table(table)
    return table
def select_operation_multiple(tables, search_conditions, security_level):
    new_tables = []
    for table in tables:
        searches = []
        for cond in search_conditions:
            temp = cond.split("=")
            if temp[0] in table[0]:
                searches.append(cond)
        new_table = select_operation(table,searches,security_level)
        #display_table(new_table)
        new_tables.append(new_table)
    return new_tables
def security_clear(tables, security_level):
    #print "SECURITY LEVEL:",security_level
    new_table_list = []
    for table in tables:
        new_table = [table[0]]
        #print table[0]
        index0 = table[0].index("KC")
        index1 = table[0].index("TC")
        t = table.pop(0)
        # get other keys
        for row in table:
            if int(row[index0]) <= int(security_level) and int(row[index1]) <= int(security_level):
                new_table.append(row)
                # other security joins removals
        new_table_list.append(new_table)
    return new_table_list
def cartesian_operation(tables):
    new_table = []
    tab1 = tables[0]
    tab2 = tables[1]
    index3 = tab1[0].index("KC")
    index4 = tab2[0].index("KC")
    z = tab1[0].pop(-1)
    new_table.append(tab1[0] + tab2[0])
    tab1[0].append(z)
    tab1.pop(0)
    tab2.pop(0)
    #new_table.append(tab1[0] + tab2[0])
    for row in tab1:
        for row_x in tab2:
            #print row_x
            #print row[index3]
            #print row_x[index4]
            if row[index3] == row_x[index4]:
                TC1 = int(row[-1])
                TC2 = int(row_x[-1])
                m = max(TC1, TC2)
                z = row_x.pop(-1)
                v = row.pop(-1)
                new_row = row + row_x
                new_row.append(m)
                row.append(v)
                row_x.append(z)
                #print(new_row)
                new_table.append(new_row)
    return new_table
def get_join_conditions(tables, search_conditions):
    temp_1 = False
    temp_2 = False
    join_conditions = []
    for cond in search_conditions:
        temp = cond.split("=")
        for table in tables:
            if temp[0] in table[0]:
                temp_1 = True
            if temp[1] in table[0]:
                temp_2 = True
        if temp_1 and temp_2:
            join_conditions.append(cond)
        temp_1 = False
        temp_2 = False
    return join_conditions
def get_clearance_conditions(search_conditions):
    clearance_conditions = []
    for conds in search_conditions:
        temp = conds.split("=")
        if temp[0] == "KC" or temp[0] ==  "TC":
            clearance_conditions.append(conds)
    return clearance_conditions
def get_regular_conditions(search_conditions, join, clear):
    regular_conditions = []
    for cond in search_conditions:
        if cond not in clear and cond not in join:
            regular_conditions.append(cond)
    return regular_conditions
def join_operation(tables, join_conditions):
    new_table = []
    if not join_conditions and len(tables) > 1:
        return cartesian_operation(tables)
    else:
        if len(tables) == 1:
            return tables[0]
        else:
            # join_conditions = get_join_conditions(tables,search_conditions)
            for cond in join_conditions:
                #print tables
                temp = cond.split("=")
                tab1 = []
                tab2 = []
                for table in tables:
                    if temp[0] in table[0]:
                        tab1 = table
                    if temp[1] in table[0]:
                        tab2 = table
                if tab1 != tab2:
                    new_table = []
                    tables.pop(tables.index(tab1))
                    tables.pop(tables.index(tab2))
                    index1 = tab1[0].index(temp[0])
                    index2 = tab2[0].index(temp[1])
                    index3 = tab1[0].index("KC")
                    index4 = tab2[0].index("KC")
                    r = tab1[0].pop(-1)
                    new_table.append(tab1[0] + tab2[0])
                    tab1[0].append(r)
                    for row in tab1:
                        for row_x in tab2:
                            if row[index1] == row_x[index2] and row[index3] == row_x[index4]:
                                TC1 = int(row[-1])
                                TC2 = int(row_x[-1])
                                m = max(TC1, TC2)
                                z = row_x.pop(-1)
                                v = row.pop(-1)
                                new_row = row + row_x
                                new_row.append(m)
                                row.append(v)
                                row_x.append(z)
                                new_table.append(new_row)
                    #print("new table:", new_table)
                    tables.append(new_table)
                else:
                    index1 = tab1[0].index(temp[0])
                    index2 = tab1[0].index(temp[1])
                    for row in tab1[1:]:
                        if row[index1] != row[index2]:
                            tab1.pop(tab1.index(row))
                            new_table = tab1[:]
            return new_table
def parse_query(query):
    """
    :param query: Query input from stdin 
    """
    query = query.split("SELECT", 1)
    query = query[1]
    query = query.split("FROM", 1)
    attribute_list = query[0]  # everything after the select to the from
    attribute_list = attribute_list.split(",")

    query = query[1]
    query = query.split("WHERE", 1)
    table_list = query[0]
    if len(query) > 1:
        table_list = table_list.split(",")
        search_conditions = query[1]  # everything after the where
        search_conditions = search_conditions[:-1]  # get rid of semicolon at end of query
        search_conditions = search_conditions.split("and")
    else:
        table_list = table_list[:-1]
        table_list = table_list.split(",")
        search_conditions = []

    #print "\nattribute list:", attribute_list, "\ntable_list:", table_list, "\nsearch_conditions:", search_conditions
    return attribute_list, table_list, search_conditions
def split_conditions(tables, search_conditions):
    conditions = []
    conditions.append(get_join_conditions(tables, search_conditions))
    conditions.append(get_clearance_conditions(search_conditions))
    conditions.append(get_regular_conditions(search_conditions, conditions[0], conditions[1]))
    return conditions
def security_cond_operation(table, sec_cond,security_level):
    for cond in sec_cond:
        temp = cond.split("=")
        if temp[0] == "TC" and int(temp[1]) > int(security_level):
            print "Error: Security Level Violation"
            exit()
        index = table[0].index(temp[0])
        table = make_table(table, index, temp[1])
    return table
def execute_query():
    # type: () -> object
    security_level = raw_input("Provide Security Level: ")
    while security_level != '1' and security_level != '2' and security_level != '3' and security_level != '4':
        print "Error: Security Level Must BE 1,2,3,or 4..."
        security_level = raw_input("Provide Security Level: ")
    query = raw_input("Provide Query: ").replace(" ", "")
    while not query.endswith(";"):
        query = query + raw_input().replace(" ", "")
    attribute_list, table_list, search_conditions = parse_query(query)
    tables = get_tables(table_list)
    tables = security_clear(tables, security_level)
    conditions = split_conditions(tables,search_conditions)
    security_cond = conditions[1]
    join_cond = conditions[0]
    regular_cond = conditions[2]
    #print join_cond, security_cond, regular_cond
    tables = select_operation_multiple(tables, regular_cond, security_level)

    table = join_operation(tables, join_cond)
    #with open("output.txt", "w") as output:
    #    for table in tables:
     #       for row in table:
     #           output.write("%s\n" % row)
    n_table = security_cond_operation(table,security_cond,security_level)[:]
    x_table = project_operation(n_table, attribute_list)[:]
    display_table(x_table)

with open("T1.txt", "r") as F1:
    table1 = F1.readlines()
with open("T2.txt", "r") as F2:
    table2 = F2.readlines()
with open("T3.txt", "r") as F3:
    table3 = F3.readlines()
table1[:] = [x.split() for x in table1]
table2[:] = [x.split() for x in table2]
table3[:] = [x.split() for x in table3]
o_table1 = table1[:]
o_table2 = table2[:]
o_table3 = table3[:]

#print(table1[0], " ", table2[0], " ", table3[0])
#print(table1[1], " ", table2[1], " ", table3[1])
while(True):
    execute_query()
    table1 = o_table1[:]
    table2 = o_table2[:]
    table3 = o_table3[:]
    e = raw_input("\nContinue? (y/n): ")
    e.replace(" ","")
    if e == "n":
        print "exiting..."
        break

