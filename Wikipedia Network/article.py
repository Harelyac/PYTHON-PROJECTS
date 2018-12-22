class Article:
    """
    The constructor of Article make an Article object that consist of 2 fields
    which are title and neighbor - a list that contains more Article objects!
    """
    def __init__(self, article_title):
        self.__title = article_title
        self.__neighbors = []

    def get_title(self):
        """
        This function gets the title of an Article
        :return:
        """
        return self.__title

    def add_neighbor(self,neighbor):
        """
        This function add neighbor to Article neighbor list
        :param neighbor:
        :return:
        """
        # check if new neighbor is already listed under article neighbors!
        if neighbor not in self.__neighbors:
            self.__neighbors.append(neighbor)

    def get_titles(self):
        """
        returns the names of all the neighbors
        :return:
        """
        return [neighbor.get_title() for neighbor in self.get_neighbors()]


    def get_neighbors(self):
        """
        This functions returns a list of all Article neighbors.
        :return:
        """
        return self.__neighbors

    def __repr__(self):
        """This is a magic method that used to represent the Article object
        with the Article title and Article's neighbors"""
        names_list = list()
        for neighbor in self.__neighbors:
            names_list.append(neighbor.get_title())
        repr_string = self.get_title(), names_list
        return str(repr_string)

    def __len__(self):
        """
        This function, returns the number of neighbors of an Article
        :return:
        """
        num_of_neighbors = len(self.__neighbors)
        return num_of_neighbors

    def __contains__(self, article):
        """
        This magic method check whether an article is a neighbor of the
        current Article.
        :param article:
        :return:
        """
        if article in self.__neighbors:
            return True
        else:
            return False



