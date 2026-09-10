from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import TripMember
from ..factories import TripFactory, TripMemberFactory, UserFactory


class TripModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.trip = TripFactory(owner=self.user)

    def test_str_method(self):
        self.assertEqual(str(self.trip), f"{self.trip.title} - {self.trip.destination}")

    def test_created_at_is_set(self):
        self.assertIsNotNone(self.trip.created_at)

    def test_end_date_before_start_date_raises_error(self):
        with self.assertRaises(ValidationError):
            TripFactory(owner=self.user, start_date="2026-07-14", end_date="2026-07-01")

    def test_same_start_and_end_date_is_valid(self):
        trip = TripFactory(
            owner=self.user, start_date="2026-07-01", end_date="2026-07-01"
        )
        self.assertEqual(trip.start_date, trip.end_date)

    def test_is_owner_returns_true(self):
        self.assertTrue(self.trip.is_owner(self.user))

    def test_is_owner_returns_false_for_other_user(self):
        other = UserFactory()
        self.assertFalse(self.trip.is_owner(other))

    def test_is_participant_returns_true_for_member(self):
        member = UserFactory()
        TripMemberFactory(trip=self.trip, user=member)
        self.assertTrue(self.trip.is_participant(member))

    def test_owner_tripmember_created_on_save(self):
        self.assertTrue(
            TripMember.objects.filter(trip=self.trip, user=self.user).exists()
        )
