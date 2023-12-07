from django.test import TestCase
from django.urls import reverse
from .models import Member

# Model Test
class MemberModelTest(TestCase):
  def test_isAdmin_return_true(self):
    admin_member = Member(role="admin")
    self.assertIs(admin_member.isAdmin(), True)

  def test_isAdmin_return_false(self):
    admin_member = Member(role="regular")
    self.assertIs(admin_member.isAdmin(), False)

# Views Test
class MemberAddViewTests(TestCase):
  def test_add_member(self):
    member = Member.objects.create(
      id=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      role="regular")
    response = self.client.get(reverse("teammanager:index"))
    self.assertQuerySetEqual(response.context["existing_members"], [member])

class MemberIndexViewTests(TestCase):
  def test_display_no_member_message(self):
    response = self.client.get(reverse("teammanager:index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No members are added.")
    self.assertQuerySetEqual(response.context["existing_members"], [])
    
  def test_display_num_of_members(self):
    member1 = Member.objects.create()
    member2 = Member.objects.create()
    memberList = [member1, member2]
    response = self.client.get(reverse("teammanager:index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "You have "+ str(len(memberList)) +" team members.")
    self.assertQuerySetEqual(response.context["existing_members"], memberList)

class MemberEditViewTests(TestCase):
  def test_display_edit_view(self):
    Member.objects.create(id=1)
    response = self.client.get(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Edit team member")

  def test_not_existed_member(self):
    Member.objects.create(id=1)
    response = self.client.get(reverse("teammanager:edit", kwargs={'pk': 2}))
    self.assertEqual(response.status_code, 404)
  
  def test_display_values_of_member(self):
    member = Member.objects.create(
      id=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      role="regular")
    response = self.client.get(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertTemplateUsed(response, 'teammanager/edit.html')
    self.assertContains(response, "Alex")
    self.assertContains(response, "Miyake")
    self.assertContains(response, "miyake@example.com")
    self.assertContains(response, "1234-5678-90")
    expected_html = '<input type="radio" name="role" id="regular" value="regular" checked>'
    self.assertContains(response, expected_html, html=True)

  def test_edit_fname(self):
    member = Member.objects.create(
      pk=1,
      first_name="Alex"
    )
    member.first_name = "Tate"
    self.client.post(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertEqual(member.first_name, "Tate")
    self.assertNotEqual(member.first_name, "Alex")

  def test_edit_lname(self):
    member = Member.objects.create(
      pk=1,
      last_name="Miyake"
    )
    member.last_name = "Tate"
    self.client.post(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertEqual(member.last_name, "Tate")
    self.assertNotEqual(member.last_name, "Alex")

  def test_edit_email(self):
    member = Member.objects.create(
      pk=1,
      email="miyake@example.com"
    )
    member.email = "tate@example.com"
    self.client.post(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertEqual(member.email, "tate@example.com")
    self.assertNotEqual(member.email, "miyake@example.com")

  def test_edit_location(self):
    member = Member.objects.create(
      pk=1,
      location="1234-5678-90"
    )
    member.location = "8888-8888-90"
    self.client.post(reverse("teammanager:edit", kwargs={'pk': 1}))
    self.assertEqual(member.location, "8888-8888-90")
    self.assertNotEqual(member.location, "1234-5678-90")

  def test_edit_role(self):
    member = Member.objects.create(
      pk=1,
      role="regular"
    )
    member.role = "admin"
    self.client.post("/teammanager/edit_member/", kwargs={'pk': 1})
    self.assertEqual(member.isAdmin(), True)
    self.assertNotEqual(member.isAdmin(), False)

class MemberDeleteViewTests(TestCase):
  def test_delete_member(self):
    Member.objects.create(
      pk=1,
      first_name="Alex",
      last_name="Miyake",
      email="miyake@example.com",
      location="1234-5678-90",
      role="regular")
    Member.objects.create(
      pk=2,
      first_name="Jason",
      last_name="Douglas",
      email="Douglas@example.com",
      location="1234-5678-90",
      role="regular")
    response = self.client.post(reverse("teammanager:delete_member", kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 302)