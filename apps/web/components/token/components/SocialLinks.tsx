"use client";

import {

    Globe,

    Send,

    Twitter,

    Github

} from "lucide-react";

interface Props {

    website?: string;

    telegram?: string;

    twitter?: string;

    github?: string;

}

export default function SocialLinks({

    website,

    telegram,

    twitter,

    github

}: Props) {

    const links = [

        {
            icon: Globe,
            href: website
        },

        {
            icon: Send,
            href: telegram
        },

        {
            icon: Twitter,
            href: twitter
        },

        {
            icon: Github,
            href: github
        }

    ];

    return (

        <div className="flex gap-3">

            {

                links

                    .filter(link => link.href)

                    .map((link, index) => (

                        <a

                            key={index}

                            href={link.href}

                            target="_blank"

                            className="rounded-lg bg-[#1B2330] p-3 hover:bg-[#263244]"

                        >

                            <link.icon size={20} />

                        </a>

                    ))

            }

        </div>

    );

}