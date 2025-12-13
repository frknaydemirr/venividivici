export  class  MenuModel{
      name: string = "";
  icon: string | undefined = "";
  url: string = "";
  isTitle: boolean = false;
  subMenus: MenuModel[] = [];
}

export const Menus: MenuModel[] = [
  {
    name: "Anasayfa",
    icon: "fa  fa-solid fa-home",
    url: "/home",
    isTitle: false,
    subMenus: []
  },

  {
    name: "Şehirler",
    icon: "fa-solid fa-clipboard-list",
    url: "/cities",
    isTitle: false,
    subMenus: []
  },

  {
     name: "Ülkeler",
    icon: "fa-solid fa-screwdriver-wrench",
    url: "/countries",
    isTitle: false,
    subMenus: []
  },
    {
     name: "soruCevaplar",
    icon: "fa-solid fa-screwdriver-wrench",
    url: "/answersorquestions",
    isTitle: false,
    subMenus: []
  },
      {
     name: "girişyap",
    icon: "fa-solid fa-screwdriver-wrench",
    url: "/login",
    isTitle: false,
    subMenus: []
  }
];
