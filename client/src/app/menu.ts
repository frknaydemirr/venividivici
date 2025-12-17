export class MenuModel {
  name: string = "";
  icon: string = "";
  url: string = "";
  isTitle: boolean = false;
  subMenus: MenuModel[] = [];
}

export const Menus: MenuModel[] = [
  {
    name: "Home",
    icon: "fa fa-solid fa-home",
    url: "/home",
    isTitle: false,
    subMenus: []
  },
  {
    name: "Cities",
    icon: "fa-solid fa-clipboard-list",
    url: "/cities",
    isTitle: false,
    subMenus: []
  },
  {
    name: "Countries",
    icon: "fa-solid fa-screwdriver-wrench",
    url: "/countries",
    isTitle: false,
    subMenus: []
  },
  {
    name: "AnswerOrQuestions",
    icon: "fa-solid fa-screwdriver-wrench",
    url: "/question-or-answers",
    isTitle: false,
    subMenus: []
  },

];