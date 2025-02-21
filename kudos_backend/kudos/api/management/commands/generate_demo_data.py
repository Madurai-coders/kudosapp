from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Kudos, KudosQuota
from faker import Faker
import random

fake = Faker()

MAX_KUDOS_PER_WEEK = 3  # Ensure this matches your settings


class Command(BaseCommand):
    help = "Flush existing data (except admin) and generate random demo data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Flushing existing non-admin data...")

        # Delete all KudosQuota records first to prevent UNIQUE constraint errors
        KudosQuota.objects.all().delete()

        # Exclude superusers (admins) from deletion
        non_admin_users = User.objects.filter(is_superuser=False)

        # Delete all related Kudos first (to avoid foreign key issues)
        Kudos.objects.filter(giver__in=non_admin_users).delete()
        Kudos.objects.filter(receiver__in=non_admin_users).delete()

        # Delete users who are not admins
        deleted_users_count, _ = non_admin_users.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_users_count} non-admin users and related data!"))

        self.stdout.write("Generating new users...")

        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"
            )
            users.append(user)

        # Ensure quotas are created for each new user without duplicates
        for user in users:
            KudosQuota.objects.get_or_create(user=user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})

        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} new users!"))

        self.stdout.write("Generating Kudos...")
        for _ in range(20):
            sender, receiver = random.sample(users, 2)

            # Fetch sender's quota
            quota, _ = KudosQuota.objects.get_or_create(user=sender, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})

            if quota.kudos_remaining > 0:  # Only create kudos if quota is available
                Kudos.objects.create(
                    giver=sender,
                    receiver=receiver,
                    message=fake.sentence()
                )
                quota.kudos_remaining -= 1  # Reduce kudos count
                quota.save(update_fields=["kudos_remaining"])  # Save updated quota

        self.stdout.write(self.style.SUCCESS("Demo data successfully created!"))
