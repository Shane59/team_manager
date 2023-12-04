from django.test import TestCase
from django.urls import reverse
from .models import Member

# Model Test
class MemberModelTest(TestCase):
  def test_is_admin_with_admin(self):
    # isAdmin returns false when is_admin is false
    admin_member = Member(is_admin=True)
    self.assertIs(admin_member.isAdmin(), True)
  def test_is_admin_with_nonadmin(self):
    # isAdmin returns false when is_admin is false
    admin_member = Member(is_admin=False)
    self.assertIs(admin_member.isAdmin(), False)

# Views Test
class MemberIndexViewTests(TestCase):
  def test_display_no_member_message(self):
    response = self.client.get("/teammanager/")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No members are added.")
    self.assertQuerySetEqual(response.context["existing_members"], [])
    
  def test_display_num_of_members(self):
    member1 = Member.objects.create()
    member2 = Member.objects.create()
    memberList = [member1, member2]
    response = self.client.get("/teammanager/")
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "You have "+ str(len(memberList)) +" team members.")
    self.assertQuerySetEqual(response.context["existing_members"], memberList)

class MemberEditViewTests(TestCase):
  def test_not_existed_member(self):
    Member.objects.create(id=1)
    url = "/teammanager/edit/" + str(2)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)
  
  def test_display_edit_view(self):
    Member.objects.create(id=1)
    response = self.client.get("/teammanager/edit/1")
    self.assertContains(response, "Edit team member")

  def test_display_values_of_member(self):
    Member.objects.create(
      id=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      is_admin=False)
    response = self.client.get("/teammanager/edit/1")
    self.assertTemplateUsed(response, 'teammanager/edit.html')
    self.assertContains(response, "Alex")
    self.assertContains(response, "Miyake")
    self.assertContains(response, "miyake@example.com")
    self.assertContains(response, "1234-5678-90")

  def test_edit_member(self):
    member = Member.objects.create(
      pk=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      is_admin=False)
    member.first_name = "Tate"
    response = self.client.post("/teammanager/edit_member/", kwargs={'pk': 1})
    self.assertEqual(member.first_name, "Tate")
    self.assertNotEqual(member.first_name, "Alex")

  def test_delete_member(self):
    member1 = Member.objects.create(
      pk=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      is_admin=False)
    member2 = Member.objects.create(
      pk=2,
      first_name="Jason",
      last_name="Douglas",
      email="Douglas@example.com",
      location="1234-5678-90",
      is_admin=False)
    response = self.client.get(reverse("teammanager:delete_member", kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 302)