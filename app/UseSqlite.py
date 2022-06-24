###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################


# Reference: Dusty Phillips.  Python 3 Objected-oriented Programming Second Edition. Pages 326-328.
# Copyright (C) 2019 Hui Lan

import sqlite3

class Sqlite3Template:
    def __init__(self, db_fname):
        self.db_fname = db_fname

    def connect(self, db_fname):
        self.conn = sqlite3.connect(self.db_fname)

    def instructions(self, query_statement):
        raise NotImplementedError()

    def operate(self):
        self.conn.row_factory = sqlite3.Row
        self.results = self.conn.execute(self.query) # self.query is to be given in the child classes
        self.conn.commit()

    def format_results(self):
        raise NotImplementedError()

    def do(self):
        self.connect(self.db_fname)
        self.instructions(self.query)
        self.operate()

    def instructions_with_parameters(self, query_statement, parameters):
        self.query = query_statement
        self.parameters = parameters

    def do_with_parameters(self):
        self.connect(self.db_fname)
        self.instructions_with_parameters(self.query, self.parameters)
        self.operate_with_parameters()

    def operate_with_parameters(self):
        self.conn.row_factory = sqlite3.Row
        self.results = self.conn.execute(self.query, self.parameters) # self.query is to be given in the child classes
        self.conn.commit()


class InsertQuery(Sqlite3Template):
    def instructions(self, query):
        self.query = query


class RecordQuery(Sqlite3Template):
    def instructions(self, query):
        self.query = query

    def format_results(self):
        output = []
        for row_dict in self.results.fetchall():
            lst = []
            for k in dict(row_dict):
                lst.append( row_dict[k] )
            output.append(', '.join(lst))
        return '\n\n'.join(output)

    def get_results(self):
        result = []
        for row_dict in self.results.fetchall():
            result.append( dict(row_dict) )
        return result



if __name__ == '__main__':

    #iq = InsertQuery('RiskDB.db')
    #iq.instructions("INSERT INTO inspection Values ('FoodSupplies', 'RI2019051301', '2019-05-13', '{}')")
    #iq.do()
    #iq.instructions("INSERT INTO inspection Values ('CarSupplies', 'RI2019051302', '2019-05-13', '{[{\"risk_name\":\"elevator\"}]}')")
    #iq.do()

    rq = RecordQuery('wordfreqapp.db')
    rq.instructions("SELECT * FROM article WHERE level=3")
    rq.do()
    #print(rq.format_results())
