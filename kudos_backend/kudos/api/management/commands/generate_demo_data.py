from django.core.management.base import BaseCommand
from api.models import Kudos, KudosQuota, Organization
from faker import Faker
import random
from django.contrib.auth import get_user_model
User = get_user_model()


fake = Faker()

MAX_KUDOS_PER_WEEK = 3  # Ensure this matches your settings


class Command(BaseCommand):
    help = "Flush existing data (except admin) and generate random demo data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Flushing existing non-admin data...")

        # Delete all KudosQuota records first to prevent UNIQUE constraint errors
        KudosQuota.objects.all().delete()

        # Delete all Kudos
        Kudos.objects.all().delete()

        # Exclude superusers (admins) from deletion
        non_admin_users = User.objects.filter(is_superuser=False)

        # Delete users who are not admins
        deleted_users_count, _ = non_admin_users.delete()

        # Delete old organizations
        Organization.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_users_count} non-admin users and related data!"))

        self.stdout.write("Generating new organizations...")

        organizations = [Organization.objects.create(name=fake.company()) for _ in range(3)]

        self.stdout.write(self.style.SUCCESS(f"Created {len(organizations)} organizations!"))

        self.stdout.write("Generating new users...")

        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"
            )
            user.organization = random.choice(organizations)  # Assign user to a random organization
            user.save()
            users.append(user)

        # Ensure quotas are created for each new user
        for user in users:
            KudosQuota.objects.get_or_create(user=user, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})

        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} new users!"))

        self.stdout.write("Generating Kudos...")

        for _ in range(20):
            org_users = random.choice(organizations).user_set.all()  # Get users from the same organization

            if len(org_users) >= 2:
                sender, receiver = random.sample(list(org_users), 2)  # Ensure kudos stay within the same org

                quota, _ = KudosQuota.objects.get_or_create(user=sender, defaults={"kudos_remaining": MAX_KUDOS_PER_WEEK})

                if quota.kudos_remaining > 0:
                    Kudos.objects.create(
                        giver=sender,
                        receiver=receiver,
                        message=fake.sentence()
                    )
                    quota.kudos_remaining -= 1
                    quota.save(update_fields=["kudos_remaining"])

        self.stdout.write(self.style.SUCCESS("Demo data successfully created!"))
