#
#   Imports
#

from graphiti_core.nodes import EpisodeType
import ollama

from datetime import datetime, timezone
from typing import List

# Perso

from facts_database.bootstrap import bootstrap_graphiti
from async_worker import bootstrap_async_worker

#
#   Errors
#

class AddEpisodeError(Exception):
    """
        Error when adding an episode to the graphiti.
    """

    def __init__(self, sub_error: Exception):
        self.sub_error = sub_error
        super().__init__(
            f"Error when adding an episode to the graphiti: {sub_error}"
        )

#
#   Facts memory service
#

async_worker = bootstrap_async_worker()

class FactsMemoryService:
    """
        Facts memory service class. It stores the facts of the user
        with a time stamp and validity. It is a form of graph that
        evolves over time. Each message is analysed to extract the facts,
        entities and relations. Then compares and stores in the graph.

        It relies mostly on the Graphiti library to manage the graph and 
        the neo4j to store the graph in the database.
    """

    def __init__(self):
        self._graphiti = bootstrap_graphiti()

    def extract_and_save_facts(
        self,
        window: List[ollama.Message]
    ) -> None:
        """
            Extracts and saves the facts from the window.

            Params:
                - window: The window of messages to extract the 
                facts from. It is a list of Ollama messages.

            Raises:
                - AddEpisodeError: If the episode cannot be added to
                the graphiti.
        """

        #
        #   Preparing the payload
        #
        
        payload = ""
        for msg in window:
            payload += f"{msg.role}: {msg.content}\n"

        #
        #   Adding the episode
        #

        now = datetime.now(timezone.utc)

        try:
            async_worker.run(
                self._graphiti.add_episode(
                    # TODO: Better naming system with llm inference for instance
                    name=f"jarvis_conversation_{now.strftime('%Y%m%d%H%M%S_%f')}",
                    episode_body=payload,
                    source=EpisodeType.message,
                    source_description="Jarvis conversation",
                    reference_time=now,
                )
            )
        except Exception as e:
            raise AddEpisodeError(e) from e

    def search_facts(
        self,
        query: str
    ) -> List[str]:
        """
            Searches the facts in the graphiti.

            Params:
                - query: The query to search the facts from.

            Returns:
                - A list of the facts found in the graphiti.
        """

        edges = async_worker.run(self._graphiti.search(query))

        print(edges) # TODO: Remove this

        facts = [edge.fact for edge in edges]

        return facts