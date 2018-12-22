from article import *


class WikiNetwork:
    """
    This class makes the whole Wikipedia network!
    """
    def __init__(self, link_list):
        self.__network = {} # The Wikipedia network
        self.update_network(link_list) # Update the network first

    def update_network(self, link_list):
        """
        This method make the full network come to life
        :param link_list:
        :return:
        """
        network = self.__network
        for (article, neighbor) in link_list:
            if article not in network:
                network[article] = Article(article)
            if neighbor not in network:
                network[neighbor] = Article(neighbor)
            network[article].add_neighbor(network[neighbor])

    def get_articles(self):
        """
        This method returns all articles inside the network.
        :return:
        """
        return list(self.__network.values())

    def get_titles(self):
        """
        This method returns all titles of articles inside the network.
        :return:
        """
        return list(self.__network.keys())

    def __contains__(self, title):
        """
        This method checks if article exist in network based on its title.
        :param title:
        :return:
        """
        if title in self.__network.keys():
            return True
        else:
            return False

    def __len__(self):
        """
        This method returns the number of articles inside the network.
        :return:
        """
        return len(self.__network)

    def __repr__(self):
        """
        This method return string that represent the network.
        :return:
        """
        return str(self.__network)

    def __getitem__(self, title):
        """
        This method return an object that correspond the given title name.
        else it will raise an error.
        :param title:
        :return:
        """
        if title in self.__network.keys():
            return self.__network[title]
        else:
            raise KeyError(title)

    def page_rank(self, iters, d = 0.9):
        """
        Calculates the page rank of the articles in the network
        and returns a list of article names by sorted by descending
        Page rank and by ascending lexicographical order
        """
        network = self.__network
        rank = {article: 1 for article in network}
        # this dict is used to sum
        cur_iter = {article: 0 for article in network}

        for iter in range(iters):
            for name, article in network.items():
                # Calculate the amount to be divided between neighbors.
                if len(article) > 0:
                    div_amount = (rank[name] * d) / len(article)
                    # decrease money from Giver
                    rank[name] = 1 - d
                    # Going over each neighbor and spread money
                    for neighbor in article.get_neighbors():
                        cur_iter[neighbor.get_title()] += div_amount
            # spread all the money to their true owners!
            for article in cur_iter:
                rank[article] += cur_iter[article]
                cur_iter[article] = 0
        return [item[0] for item in sorted(rank.items(),
                                           key=lambda i: (-i[1], i[0]))]

    def jaccard_index(self, article_name):
        """
        Calculates the Jaccard index of a given article with the entire
        network. Returns a list of article names sorted by their Jaccard
        index and then by ascending lexicographical order
        """
        network = self.__network

        # Check if article title not in network keys.
        if article_name not in network:
            return None

        # Check if article got no neighbors
        if len(network[article_name]) == 0:
            return None

        def _jaccard_index(article1_neighbors, article2):
            """
            An inner function that calculates the Jaccard Index between
            a certain article and a given list of neighbors
            """

            n = [set(article1_neighbors),
                 set(network[article2].get_neighbors())]
            return len(set.intersection(*n)) / len(set.union(*n))

        jaccard_rank = {article: _jaccard_index
        (network[article_name].get_neighbors(),
         article) for article in network}
        return [item[0] for item in sorted(jaccard_rank.items(),
                                           key=lambda i: (-i[1], i[0]))]

    def _entrance_level(self, article_name):
        network = self.__network
        return sum(1 if article_name in network[article].get_titles() else 0
                   for article in network)

    def travel_path_iterator(self, article_name):
        """
        Returns an iterator for traveling in the network from a given
        article in the network by entrance rank in the network.
        """
        network = self.__network
        if article_name not in network:
            return iter(())
        yield article_name

        # run until we set into an article with zero neighbors
        while len(network[article_name]) > 0:
            entrance_rank = {art: self._entrance_level(art)
            for art in network[article_name].get_titles()}
            article_name = sorted(entrance_rank.items(),
                                  key=lambda i: (-i[1], i[0]))[0][0]
            yield article_name

    def friends_by_depth(self, article_name, depth):
        """
        Returns all the level-n (n = depth) neighbors of a given article,
        where level-n neighbors denote all the neighbors you can get to in
        n steps or less from the original article.
        """
        network = self.__network
        if article_name not in network:
            return None
        neighbors = {article_name}
        for _ in range(depth):
            for article in list(neighbors):
                for n in network[article].get_neighbors():
                    title_of_n = n.get_title()
                    neighbors.add(title_of_n)
        return list(neighbors)


def read_article_links(file_name):
    """
    This functions read article links from specific given file. it sort each
    pair of links into one tuple. which makes of a lot of tuples.
    :param file_name:
    :return: A list which its objects are all pairs of articles.
    """
    all_article_pairs = list()
    with open(file_name, 'r') as article_file:
        for file_current_line in article_file.readlines():
            two_article_list = file_current_line.split()
            pair = two_article_list[0], two_article_list[1]
            all_article_pairs.append(pair)
    article_file.close()
    return all_article_pairs
