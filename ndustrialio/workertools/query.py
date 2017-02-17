class Query(object):
    def __init__(self, table_name):

        self._verb = None
        self._from = table_name
        self._fields = []
        self._joins = []
        self._wheres = None
        self._order = None
        self._limit = None
        self._args = None
        self._group_by = None
        self._subqueries = []

    def table(self):

        return self._from

    def verb(self, verb=None):

        if verb is None:
            return self._verb

        else:
            self._verb = verb

            return self

    def group_by(self, columns):
        """
        Args:
            columns: list of string or string

        Returns: the Query object
        """
        if type(columns) in [list, str]:
            self._group_by = columns
        else:
            raise TypeError("'columns' argument should be either a list of strings or a string")
        return self

    def fields(self, field=None):

        if field is None:
            return self._fields

        elif type(field) in [list, tuple]:
            self._fields.extend(field)
            return self
        else:
            self._fields.append(field)
            return self

    def where(self, where=None):
        if where is None:
            return self._wheres
        else:
            self._wheres = where
            return self

    def order(self, column=None, desc=None):

        if column is None and desc is None:

            return self._order
        else:
            if desc:
                self._order = 'ORDER BY ' + column + ' DESC'
            else:
                self._order = 'ORDER BY ' + column

            return self

    def join(self, join_from=None, join_table=None, join_conditions=None, join_list=None):

        if join_list is not None:

            self._joins = join_list[:]

            return self

        else:

            if join_table is None and join_conditions is None:
                # return join list
                return self._joins

            else:

                if join_from is None:
                    join_from = self._from

                processed_conditions = []

                # Create condition strings
                for condition in join_conditions:

                    left_cond = condition[0]
                    right_cond = condition[1]

                    if isinstance(left_cond, Cast):
                        left_cond = str(left_cond.table(join_from))
                    else:
                        left_cond = join_from + '.' + left_cond

                    if isinstance(right_cond, Cast):
                        right_cond = str(right_cond.table(join_table))
                    else:
                        right_cond = join_table + '.' + right_cond

                    processed_conditions.append(left_cond + ' = ' + right_cond)

                self._joins.append('JOIN ' + join_table + ' ON ' + ' AND '.join(processed_conditions))

                return self

    def left_join(self, join_from=None, join_table=None, join_conditions=None):


        if join_table is None and join_conditions is None:
            return self._joins

        else:

            if join_from is None:
                join_from = self._from

            processed_conditions = []

            # Create condition strings
            for condition in join_conditions:

                left_cond = condition[0]
                right_cond = condition[1]

                if isinstance(left_cond, Cast):
                    left_cond = str(left_cond.table(join_from))
                else:
                    left_cond = join_from + '.' + left_cond

                if isinstance(right_cond, Cast):
                    right_cond = str(right_cond.table(join_table))
                else:
                    right_cond = join_table + '.' + right_cond

                processed_conditions.append(left_cond + ' = ' + right_cond)

            self._joins.append('LEFT JOIN ' + join_table + ' ON ' + ' AND '.join(processed_conditions))

            return self

    
    def limit(self, limit=None):

        if limit is None:
            return self._limit

        else:
            self._limit = limit

            return self

    def args(self, args=None):

        if args is None:
            return self._args

        else:
            self._args = args

            return self

    def subquery(self, name, query):


        if not self._subqueries:
            # Do this differently for the first subquery
            self._subqueries.append('WITH ' +
                                    name +
                                ' AS (' + str(query) +')')
        else:
            self._subqueries.append(name +
                                   ' AS  (' +
                                    str(query) + ')')

        return self

    def __str__(self):

        query_chunks = []

        # Do subqueries first
        query_chunks.append(', '.join(self._subqueries))

        query_chunks.append(self._verb)

        query_chunks.append(', '.join(self._fields))

        query_chunks.append('FROM ' + self._from)

        if self._joins:
            query_chunks.append(' '.join(self._joins))

        if self._wheres:
            query_chunks.append(str(self._wheres))

        if self._group_by is not None:
            query_chunks.append('GROUP BY ' + (','.join(self._group_by) if type(self._group_by) is list else self._group_by))

        if self._limit:
            query_chunks.append('LIMIT ' + str(self._limit))

        if self._order:
            query_chunks.append(self._order)

        query_str = ' '.join(query_chunks)

        if self._args is not None:
            query_str = query_str.format(self._args)

        return query_str



class Update(Query):

    def __init__(self, table_name):

        super(Update, self).__init__(table_name)

        self._verb = 'UPDATE'

        self._values = []

    def values(self, values=None):

        if values is None:

            return self._values
        else:
            # try treating it as a list first
            try:
                self._values.extend(values)
            except TypeError:
                self._values.append(values)

    def __str__(self):

        query_chunks = []
        query_chunks.append(self._verb)
        query_chunks.append(self._from)
        query_chunks.append('SET')

        if len(self._values) != len(self._fields):

            # insert wildcards
            f = ['='.join((x, '%s')) for x in self._fields]

        else:

            f = ['='.join((x, y)) for x, y in zip(self._fields, self._values)]

        query_chunks.append(', '.join(f))

        if self._wheres:
            query_chunks.append(str(self._wheres))


        query_str = ' '.join(query_chunks)

        return query_str

class Select(Query):

    def __init__(self, table_name):

        super(Select, self).__init__(table_name)

        self._verb = 'SELECT'

    def __str__(self):

        query_chunks = []

        # Do subqueries first
        query_chunks.append(', '.join(self._subqueries))

        query_chunks.append(self._verb)
        query_chunks.append(', '.join(self._fields))
        query_chunks.append('FROM ' + self._from)

        if self._joins:
            query_chunks.append(' '.join(self._joins))

        if self._wheres:
            query_chunks.append(str(self._wheres))

        if self._order:
            query_chunks.append(self._order)

        if self._group_by is not None:
            query_chunks.append('GROUP BY ' + (','.join(self._group_by) if type(self._group_by) is list else self._group_by))

        if self._limit:
            query_chunks.append('LIMIT ' + str(self._limit))

        query_str = ' '.join(query_chunks)

        if self._args is not None:
            query_str = query_str.format(self._args)

        return query_str

class CQLSelect(Select):

    def __init__(self, table_name):

        super(CQLSelect, self).__init__(table_name)

    def order(self, column=None, desc=None):

        if column is None and desc is None:

            return self._order
        else:
            if desc:
                self._order = 'ORDER BY ' + column + ' DESC'
            else:
                self._order = 'ORDER BY ' + column + ' ASC'

            return self


class Count(Select):

    def __init__(self, table_name=None, query=None):

        if table_name:
            super(Count, self).__init__(table_name)

        elif query:
            super(Count, self.__init__(query.table()))

            # copy wheres and joins, but not fields
            self._wheres = query._wheres
            self._joins = query.join()
            self._subqueries = query._subqueries

        else:
            raise Exception('table_name or query must be provided!')

    def __str__(self):

        query_chunks = []

        # Do subqueries first
        query_chunks.append(', '.join(self._subqueries))


        query_chunks.append(self._verb)

        fields_str = ', '.join(self._fields)

        if fields_str:
            query_chunks.append('COUNT(' + fields_str + ')')
        else:
            query_chunks.append('COUNT(1)')

        query_chunks.append('FROM ' + self._from)

        if self._joins:
            query_chunks.append(' '.join(self._joins))

        if self._wheres:
            query_chunks.append(str(self._wheres))

        query_str = ' '.join(query_chunks)

        if self._args is not None:
            query_str = query_str.format(self._args)

        return query_str


class Where(object):
    def __init__(self, first_clause):
        if first_clause is None:
            raise Exception('First clause in WHERE cannot be none')
        self.where = 'WHERE ' + first_clause.strip()

    def AND(self, clause):
        self.where += ' AND ' + clause.strip()
        return self

    def OR(self, clause):
        self.where += ' OR '+clause.strip()
        return self

    def build(self):
        return self.__str__()

    def __str__(self):
        return self.where


class Cast(object):
    def __init__(self, column, cast_type):
        self._column = column
        self._cast_type = cast_type
        self._table = None

    def table(self, table):
        self._table = table
        return self

    def __str__(self):

        if self._table:
            return 'CAST('\
                +self._table\
                +'.'+self._column\
                +' AS '\
                + self._cast_type\
                +')'
        else:
            return 'CAST('\
                +self._column\
                +' AS '\
                + self._cast_type\
                +')'

