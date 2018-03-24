"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/")
        self.assertIn("Please RSVP", result.data)
        self.assertNotIn("San Francisco", result.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)
        self.assertNotIn("Please RSVP", result.data)
        self.assertIn("San Francisco", result.data)


    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info1 = {'name': "Jane", 'email': "jane@jane.com"}
        rsvp_info2 = {'name': "Jane", 'email': "mel@ubermelon.com"}
        rsvp_info3 = {'name': "Mel Melitpolski", 'email': "jane@jane.com"}
        rsvp_info4 = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info1, follow_redirects=True)
        self.assertNotIn("Sorry, Mel", result.data)

        result = self.client.post("/rsvp", data=rsvp_info2, follow_redirects=True)
        self.assertIn("Sorry, Mel", result.data)

        result = self.client.post("/rsvp", data=rsvp_info3, follow_redirects=True)
        self.assertIn("Sorry, Mel", result.data)

        result = self.client.post("/rsvp", data=rsvp_info4, follow_redirects=True)
        self.assertIn("Sorry, Mel", result.data)

if __name__ == "__main__":
    unittest.main()
